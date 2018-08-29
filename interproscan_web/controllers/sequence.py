from hashlib import md5


def get_sequence_id(sequence):
    hash_ = md5(sequence.encode('ascii')).hexdigest()
    return hash_
