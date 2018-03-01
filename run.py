#!/bin/env python

import sys

from data import load, store
from proc import process

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: ./run.py <inputfile> [<outputfile>]"
        sys.exit(0)

    infile = sys.argv[1]
    if len(sys.argv) == 2:
        outfile = infile.split('/')[-1].split('.')[0] + '.out'
    else:
        outfile = sys.argv[2]

    # infile = 'data/'+infile
    outfile = 'out/'+outfile

    print 'loading input from', infile
    data = load(infile)

    print 'processing ...'
    data = process(data)

    print 'storing output to', outfile
    store(outfile, data)
