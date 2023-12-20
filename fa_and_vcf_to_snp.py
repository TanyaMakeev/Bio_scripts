#!/usr/bin/env python
'''
The program takes FastA and VCF files as an input and returns SNP list with 35 bases on each side of the SNP

@author: tanya.makeev
'''

from sys import argv
(script, fafile, vcffile, outfile) = argv

key = value = ''
appends = 0
map = {}
line_number = 0

# Read FastA file and create chromosome name/sequence dictionary
with open(outfile, "w") as outf:
    with open(fafile, "r") as faf:
        for line in faf:
            line = line.strip(" \t\b\r\n");
            line = line.replace("\r", "");
            if line:
                # check is this is a chromosome name
                if line[0] is '>':
                    line = line[1:].strip(" \t\b\r")
                    line = line.lower()
                    # Print out the last key and reset it to none
                    if key:
                        print "Inserting key: %s, value size: %d" % (key, len(value))
                        map[key] = value
                        key = value = ''
                        appends = 0

                    # get chromosome name and make it a new key
                    list = line.split(' ', 1)
                    if len(list) < 1 or len(list[0]) < 1:
                        print "*** Invalid FASTA on Line %d ***\n" % line_number
                        key = '<Unknown>'
                    else:
                        key = list[0].translate(None, " \t\b\r\n");
                        print "Found key: %s" % key
                # if not a chromosome name, add the sequence as value
                else:
                    value += line.translate(None, " \t\b\r\n");
                    
            line_number += 1

    if key:
        print "Inserting key: %s, value size: %d" % (key, len(value))
        map[key] = value
    
    # Print output file header
    outf.write("SnpID\tSeventyonemer\tChromosome\tPosition\tTrue_Ref_Allele\tSubmitted_Ref_Allele\n")
    err = open ("errors.txt", "w+")
    
    # Read VCF file
    with open(vcffile, "r") as vcf:
        for line in vcf:
            line = line.strip(" \t\b\r\n");
            line = line.replace("\r", "");
            if line and line[0] is not "#":     # ignore comments
                raw = line.split('\t', 5)
                if len(raw) < 5:
                    print "Invalid line in %s: %s\n" % (vcffile, line)
                    continue
        
                # print "\n*** VCF Line:\n"
                # print line
        
                key = raw[0].translate(None, " \t\b\r\n");
                key = key.lower()
                pos = int(raw[1])
        
        
                if key in map:
                    value = map[key]
                    name = key + "_" + str(pos)
                    r3 = raw[3].translate(None, " \t\b\r\n")
                    r4 = raw[4].translate(None, " \t\b\r\n")
                    len3 = len(r3)
                    nv = "%s[%s/%s]%s" % (
                        value[max(0, pos - 36):pos - 1],
                        r3,
                        r4,
                        value[pos + len3 - 1:pos + 35 + len3 - 1]
                    )
                    true_base = value[pos - 1]
                    submit_ref = r3
                    # print "key: %s, name: %s, position: %d, new value: %s, true_base: %s\n" % (key, name, pos, nv, true_base)
                    outf.write("\t".join((name, nv, key, str(pos), true_base, submit_ref)) + "\n")
                else:
                    err.write ( "[*ERROR*] chr: %s IS MISSING for line: %s\n" % (key, line))
