# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 18:55:16 2019

The program reads FastQ file and returns k-mers and their count in the sequence.
The most repetitive k-mers are more likely to be adaptors.
k-mer length can be specified.  Default is 5.

@author: tanya.makeev
"""

import argparse
import os
import errno
import collections
from collections import OrderedDict

# define arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("fastq_fn", help="Raw sequence data in FASTQ format")
parser.add_argument("-k", default=5, help="Length of the adaptor")

args = parser.parse_args()

#read FASTQ file
def read_sequence (file):
    """
    :param file: file object
    :return (seq ID, seq): yields (seq ID, seq) tuples
    """
    name = None
    i = 0
    for line in file:
        txt = line.strip(" \b\r\n\t")
        i += 1
        if len(txt) == 0 :
            continue
        elif name is not None:
            id, name = name, None
            yield (id, txt)
        elif txt[0] == '@':
            # New seq
            name = txt[1:]
            # print ("Found FASTQ ID '%s' on line %d" % (name, i))
            
def count_kmers(read, k):
    counts = {}
    # Calculate how many kmers of length k there are
    num_kmers = len(read) - k + 1
    # Loop over the kmer start positions
    for i in range(num_kmers):
        # Slice the string to get the kmer
        kmer = read[i:i+k]
        # Add the kmer to the dictionary if it's not there
        if kmer not in counts:
            counts[kmer] = 0
        # Increment the count for this kmer
        counts[kmer] += 1
    # Return the final counts
    return counts

def main():
    try:
        f = open(args.fastq_fn)
    except IOError as e:
        print ("FASTQ file open ERROR: %s\n" % e)
        parser.print_help()
        exit(1)

    print("\nOpened FASTQ file: %s" % args.fastq_fn)
    seq_list = []
    
    with open(f, "r") as infile:
        line_ct = 0
        for line in infile:
            if (line_ct % 4 == 0):
                print("\nfound sequence" + line[1:])
                line_ct = 0
            if (line_ct  == 1):
                seq_list.append()
                line_ct += 1
    
    for seq in seq_list:
        read_counts = count_kmers(seq, args.k)
        
# dictionary sorted by value
    sorted_read_count = sorted(read_counts, key=lambda tup:tup[1], reverse=True)
    print (sorted_read_count)
    
    
    