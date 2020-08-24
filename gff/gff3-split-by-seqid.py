#!/usr/bin/env python3
import sys
import gzip

#../raw/XENTR_10.0_GCF.gff3.gz
filename_gff = "../raw/XENTR_9.1_Xenbase.gff3.gz"

f_gff = open(filename_gff, 'r')
if filename_gff.endswith('.gz'):
    f_gff = gzip.open(filename_gff, 'rt')

f_out_list = dict()
for line in f_gff:
    if line.startswith('#'):
        print(line.strip())
        continue

    tokens = line.strip().split("\t")
    tmp_chr = tokens[0].replace('Chr0', 'chr')
    if not tmp_chr.startswith('chr'):
        if tmp_chr == 'MT':
            tmp_chr = 'chrM'
        else:
            tmp_chr = 'chrUn'

    if tmp_chr not in f_out_list:
        tmp_filename_out = '../gff3/xenTro9.Xenbase_91.%s.gff3' % tmp_chr
        sys.stderr.write('Write %s\n' % tmp_filename_out)

        f_out_list[tmp_chr] = open(tmp_filename_out, 'w')
        f_out_list[tmp_chr].write('#gff-version 3\n')
        f_out_list[tmp_chr].write('#species Xenopus tropicalis\n')
        f_out_list[tmp_chr].write('#genome accession GCF_000004195.3\n')
    
    tmp_line = '%s\t%s' % (tmp_chr, '\t'.join(tokens[1:]))
    f_out_list[tmp_chr].write("%s\n" % tmp_line)
