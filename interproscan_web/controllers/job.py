import os
import bz2
import logging

from lockfile import LockFile

from interproscan_web.controllers.worker import Worker
from interproscan_web.controllers.sequence import get_sequence_id
from interproscan_web.models.error import NotDoneError, InitError

_log = logging.getLogger(__name__)


class JobManager:
    def __init__(self, data_dir=None):
        self.data_dir = data_dir
        self._worker = Worker()
        self._worker.start()

    def _get_lock(self, sequence_id):
        if self.data_dir is None:
            raise InitError("data directory is not set")

        path = os.path.join(self.data_dir, "%s.lock" % sequence_id)

        _log.debug("locking on {}".format(path))

        return LockFile(path)

    def _get_result_path(self, sequence_id):
        if self.data_dir is None:
            raise InitError("data directory is not set")

        return os.path.join(self.data_dir, "%s.xml.bz2" % sequence_id)


    def store(self, sequence_id, results):
        result_path = self._get_result_path(sequence_id)
        with self._get_lock(sequence_id):
            with bz2.open(result_path, 'wt') as f:
                f.write(results)

    def load(self, sequence_id):
        result_path = self._get_result_path(sequence_id)

        _log.debug("loading from {}".format(result_path))

        with self._get_lock(sequence_id):
            with bz2.open(result_path, 'rt') as f:
                return f.read()

    def submit(self, sequence):
        sequence_id = get_sequence_id(sequence)
        output_path = self._get_result_path(sequence_id)

        if not os.path.isfile(output_path) and not self._worker.working_on_sequence_id(sequence_id):
            self._worker.submit(sequence)

        return sequence_id


    def get_status(self, sequence_id):
        result_path = self._get_result_path(sequence_id)

        if os.path.isfile(result_path) or self._worker.result_for_sequence_id(sequence_id) is not None:
            return 'FINISHED'
        elif self._worker.working_on_sequence_id(sequence_id):
            return 'STARTED'
        elif self._worker.exception_for_sequence_id(sequence_id) is not None:
            _log.error("failure for {}: {}".format(sequence_id, self._worker.exception_for_sequence_id(sequence_id)))
            return 'FAILURE'
        elif self._worker.has_sequence_id(sequence_id):
            return 'PENDING'
        else:
            return 'NOT_FOUND'


    def get_result(self, sequence_id):
        result_path = self._get_result_path(sequence_id)
        result = self._worker.result_for_sequence_id(sequence_id)

        if os.path.isfile(result_path):
            return self.load(sequence_id)

        elif result is not None:
            self.store(sequence_id, result)

            return result
        else:
            raise NotDoneError(sequence_id)

job_manager = JobManager()
