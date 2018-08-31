import re
from hashlib import md5


def get_sequence_id(sequence):
    hash_ = md5(sequence.encode('ascii')).hexdigest()
    return hash_


SEQUENCE_PATTERN = re.compile(r"^[ACDEFGHIKLMNOPQRSTUVWY]+$")

def is_sequence(sequence):
    return SEQUENCE_PATTERN.match(sequence) is not None

