from threading import Thread, Lock
import logging

from interproscan_web.controllers.sequence import get_sequence_id
from interproscan_web.controllers.interproscan import interproscan


_log = logging.getLogger(__name__)


class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

        self._lock = Lock()
        self._queued_sequences = set()
        self._working_sequences = set()
        self._exceptions = {}
        self._results = {}

    def submit(self, sequence):
        with self._lock:
            self._queued_sequences.add(sequence)

    def has_sequence_id(self, sequence_id):
        with self._lock:
            return any([get_sequence_id(sequence) == sequence_id for sequence in (self._working_sequences | self._queued_sequences)])

    def working_on_sequence_id(self, sequence_id):
        with self._lock:
            return any([get_sequence_id(sequence) == sequence_id for sequence in self._working_sequences])

    def exception_for_sequence_id(self, sequence_id):
        with self._lock:
            if sequence_id in self._exceptions:
                return self._exceptions[sequence_id]

        return None

    def result_for_sequence_id(self, sequence_id):
        with self._lock:
            if sequence_id in self._results:
                return self._results[sequence_id]

        return None

    def run(self):
        _log.info("starting interproscan worker")
        while True:
            with self._lock:
                self._working_sequences = self._queued_sequences
                self._queued_sequences = set()

            if len(self._working_sequences) <= 0:
                continue

            try:
                results = interproscan.run(self._working_sequences)
                for sequence_id in results:
                    self._results[sequence_id] = results[sequence_id]
            except Exception as e:
                with self._lock:
                    for sequence in self._working_sequences:
                        self._exceptions[get_sequence_id(sequence)] = e
