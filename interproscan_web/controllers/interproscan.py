import tempfile
import os
import subprocess
import logging
import uuid

from interproscan_web.controllers.fasta import write_fasta
from interproscan_web.controllers.sequence import get_sequence_id


_log = logging.getLogger(__name__)


class Interproscan:
    def __init__(self, interproscan_path=None, storage_dir=None, interproscan_image=None):
        self.interproscan_path = interproscan_path
        self.storage_dir = storage_dir
        self.interproscan_image = interproscan_image

    def run(self, sequence):
        sequence_id = get_sequence_id(sequence)
        fasta_path = os.path.join(self.storage_dir, '%s.fa' % sequence_id)
        xml_path = os.path.join(self.storage_dir, '%s.xml' % sequence_id)
        container_name = "interproscan_%s" % str(uuid.uuid4())

        write_fasta(fasta_path, {sequence_id: sequence})

        try:
            self._execute(['docker', 'create', '--name',
                           container_name, self.interproscan_image,
                           self.interproscan_path, '--goterms', '--formats', 'xml',
                           '--disable-precalc',
                           '--input', "/data/%s" % os.path.basename(fasta_path),
                           '--outfile', "/data/%s" % os.path.basename(xml_path),
                           '--seqtype', 'p'])

            self._execute(['docker', 'cp', fasta_path,
                           '%s:/data/%s' % (container_name, os.path.basename(fasta_path))])

            self._execute(['docker', 'start', container_name])
            self._execute(['docker', 'wait', container_name])

            self._execute(['docker', 'cp',
                           '%s:/data/%s' %(container_name, os.path.basename(xml_path)), xml_path])

            with open(xml_path, 'r') as f:
                xml_str = f.read()
                return xml_str
        finally:
            for p in [fasta_path, xml_path]:
                if os.path.isfile(p):
                    os.remove(p)

            self._execute(['docker', 'rm', '-f', container_name])

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
