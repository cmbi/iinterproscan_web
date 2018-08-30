import os
import shutil

from nose.tools import eq_, with_setup

from interproscan_web.controllers.interproscan import interproscan
from interproscan_web import default_settings as settings


def setup():
    interproscan.interproscan_image = settings.INTERPROSCAN_IMAGE
    interproscan.interproscan_path = settings.INTERPROSCAN_PATH


def teardown():
    pass


@with_setup(setup, teardown)
def test_run():
    sequences = ["TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN",
                 "MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDR" +
                 "VKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQ" +
                 "SHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALEL" +
                 "FRKDIAAKYKELGYQG"]

    d = interproscan.run(sequences)
    eq_(len(d), 2)
