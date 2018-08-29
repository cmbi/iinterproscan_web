

def write_fasta(path, d):
    with open(path, 'w') as f:
        for key in d:
            f.write(">%s\n%s\n" % (key, d[key]))
