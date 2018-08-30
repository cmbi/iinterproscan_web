import tempfile
import os
import shutil

from nose.tools import ok_, with_setup

from interproscan_web.controllers.interproscan import interproscan
from interproscan_web import default_settings as settings


def setup():
    interproscan.interproscan_image = settings.INTERPROSCAN_IMAGE
    interproscan.interproscan_path = settings.INTERPROSCAN_PATH
    interproscan.storage_dir = tempfile.mkdtemp()


def teardown():
    if os.path.isdir(interproscan.storage_dir):
        shutil.rmtree(interproscan.storage_dir)


@with_setup(setup, teardown)
def test_run():
    sequence = "TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN"

    content = interproscan.run(sequence)
    ok_(len(content) > 0)
