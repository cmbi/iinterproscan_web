import logging

_log = logging.getLogger(__name__)


def write_fasta(path, d):
    _log.debug("writing fasta to {}".format(path))
    with open(path, 'w') as f:
        for key in d:
            f.write(">%s\n%s\n" % (key, d[key]))
