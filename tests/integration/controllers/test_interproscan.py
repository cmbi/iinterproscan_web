import tempfile
import os

from nose.tools import ok_, with_setup

from interproscan_web.controllers.interproscan import interproscan
from interproscan_web import default_settings as settings


def setup():
    interproscan.interproscan_path = settings.INTERPROSCAN_PATH


def teardown():
    pass



@with_setup(setup, teardown)
def test_run():
    sequence = "TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN"
    out_path = tempfile.mktemp()

    try:
        interproscan.run(sequence, out_path)

        ok_(os.path.isfile(out_path))
    finally:
        if os.path.isfile(out_path):
            os.remove(out_path)
