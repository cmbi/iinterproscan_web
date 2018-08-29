import tempfile
import os
import subprocess
import logging

from interproscan_web.controllers.fasta import write_fasta
from interproscan_web.controllers.sequence import get_sequence_id


_log = logging.getLogger(__name__)


class Interproscan:
    def __init__(self, interproscan_path=None, storage_dir=None):
        self.interproscan_path = interproscan_path

    def run(self, sequence, xml_path):
        sequence_id = get_sequence_id(sequence)
        fasta_path = tempfile.mktemp()
        write_fasta(fasta_path, {sequence_id: sequence})

        try:
            self._execute(fasta_path, xml_path)
        finally:
            for p in [fasta_path]:
                if os.path.isdir(p):
                    os.remove(p)

    def _execute(self, fasta_path, xml_path):

        cmd = [self.interproscan_path, '--goterms', '--formats', 'xml',
               '--disable-precalc', '--cpu', '1',
               '--input', fasta_path, '--outfile', xml_path, '--seqtype', 'p']

        _log.debug(' '.join(cmd))

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with p.stdout:
            self._log_output(p.stdout)
        p.wait()

        if p.returncode != 0:
            err_msg = p.stderr.read()
            raise RuntimeError(err_msg)


    def _log_output(self, pipe):
        for line in iter(pipe.readline, b''):  # b'\n'-separated lines
            _log.debug(line)


interproscan = Interproscan()
