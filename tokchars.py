#!/usr/bin/python3

# following
# http://victor.chahuneau.fr/notes/2012/07/03/kenlm.html

import argparse
import bz2
import glob
import sys

de_novels_dir='DE_19_novels/'


def open_f(filename):
    if filename.endswith('.bz2'):
        return bz2.open(filename, 'r')
    else: # assume it's normal tzt
        return open(filename, 'r')


# prints to stdout for piping into kenlm
def tokenize(inputfiles, lowercase):
    for fn in inputfiles:
        #print(fn)
        with open_f(fn) as f:
            for l in f:
                line = l.decode("utf-8")
                line = line.lstrip()
                # strip windowsy etc linebreak
                line = line.rstrip()
                #line = line.rstrip('\r\n')

                if lowercase:
                    line = line.lower()
                if '@' in line:
                    print('WARNING FOUND special char @', file=sys.stderr)

                if line: # avoid printing blank lines
                    # Line is deliniated into char 'words', space-separated
                    # Real spaces are replaced by @
                    print(' '.join(list(line.replace(' ','@'))))#,end='END')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--lowercase', '-l', action='store_true')
    parser.add_argument('inputfiles', nargs='*')

    args = parser.parse_args()
    if not args.inputfiles:
        print("No files given, using Novel corpus", file=sys.stderr)
        args.inputfiles = glob.glob(de_novels_dir+'*')

    tokenize(args.inputfiles, args.lowercase)


