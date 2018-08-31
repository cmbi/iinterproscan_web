import tempfile
import os
import subprocess
import logging
import uuid
import xml.etree.ElementTree as ET

from interproscan_web.controllers.fasta import write_fasta
from interproscan_web.controllers.sequence import get_sequence_id
from interproscan_web.controllers.xml import split_proteins


_log = logging.getLogger(__name__)


class Interproscan:
    def __init__(self, interproscan_path=None):
        self.interproscan_path = interproscan_path

    def run(self, sequences):
        fasta_path = tempfile.mktemp()
        xml_path = tempfile.mktemp()
        job_name = "interproscan_%s" % str(uuid.uuid4())

        write_fasta(fasta_path, {get_sequence_id(sequence): sequence for sequence in sequences})

        try:
            self._execute([self.interproscan_path, '--goterms', '--formats', 'xml',
                           '--disable-precalc',
                           '--input', fasta_path,
                           '--outfile', xml_path,
                           '--seqtype', 'p'])

            return split_proteins(xml_path)
        finally:
            for p in [fasta_path, xml_path]:
                if os.path.isfile(p):
                    os.remove(p)

    def _execute(self, cmd):
        _log.debug(' '.join(cmd))

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with p.stdout:
            self._log_output(p.stdout)
        p.wait()

        if p.returncode != 0:
            err_msg = p.stderr.read().decode('ascii')
            raise RuntimeError(err_msg)


    def _log_output(self, pipe):
        for line in iter(pipe.readline, b''):  # b'\n'-separated lines
            _log.debug(line.decode('ascii'))


interproscan = Interproscan()
