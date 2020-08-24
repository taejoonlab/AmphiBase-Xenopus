#!/usr/bin/env python3
import sys

filename_gff = sys.argv[1]

f_gff = open(filename_gff, 'r')
for line in f_gff:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    if tokens[2] == 'gene':
        print(line.strip())
f_gff.close()
