from nose.tools import ok_

from interproscan_web.controllers.sequence import is_sequence


def test_is_sequence():
    ok_(is_sequence("AAATVHIKLETWVCYS"))
    ok_(not is_sequence("#^$$%@&&$*&(*"))
