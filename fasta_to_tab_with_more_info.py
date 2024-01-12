#!/usr/bin/env python

# input: fasta file name and output tab delimited file name
# the output is going to be sequence name, description, sequence and length of sequence

from sys import argv
(script, infile, outfile) = argv

c0 = c1 = c2 = ''
with open(outfile, "w") as outf:
     with open(infile, "r") as inf:
         for line in inf:
             line = line.strip(" \t\b\r\n")
             if line:
                 if line[0] is '>':
                     line = line[1:]
                     if c0:
                         outf.write("\t".join((c0, c1, c2, str(len(c2)), "\n")))
                         c0 = c1 = c2 = ''
                     (c0, c1) = line.split(' ', 1)
                     c2 = ''
                 else:
                     c2 += line

     if c0 and c2:
         outf.write("\t".join((c0, c1, c2, str(len(c2)), "\n")))
