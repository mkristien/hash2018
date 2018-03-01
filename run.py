#!/bin/env python

from data import load, store
from proc import process

import sys

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "usage: ./run.py <inputfile> <outputfile>"
    sys.exit(0)

  infile = sys.argv[1]
  outfile = sys.argv[2]

  print 'loading input from', infile
  data = load(infile)

  print 'processing ...'
  data = process(data)

  print 'storing output to', outfile
  store(outfile, data)



