#!/usr/bin/env python3
import sys
import gzip

filename_gff_in = sys.argv[1]

sc2chr = dict()
#filename_report = '../metadata/GCF_000004195.3_Xenopus_tropicalis_v9.1_assembly_report.txt.gz'
filename_report = '../metadata/GCF_001663975.1_Xenopus_laevis_v2_assembly_report.txt.gz'

f_report = gzip.open(filename_report, 'rt')
for line in f_report:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    sc_id = tokens[0]
    chr_id = tokens[-1]
    sc2chr[sc_id] = chr_id
f_report.close()

f_gff = open(filename_gff_in, 'r')
for line in f_gff:
    tokens = line.strip().split("\t")
    tmp_sc_id = tokens[0]
    tmp_chr_id = sc2chr[tmp_sc_id]
    
    is_pseudogene = 0
    is_protein_coding = 0
    is_rna = 0

    new_attrs = []
    for tmp_attr in tokens[8].split(';'):
        if tmp_attr.startswith('ID=gene'):
            #new_attrs.append('ID=aXENTRg%07d' %
            new_attrs.append('ID=aXENLAg%07d' %
                             (int(tmp_attr.split('gene')[1])))
        elif tmp_attr.startswith('Name='):
            new_attrs.append('Name=%s' %
                             (tmp_attr.split('=')[1].lower()))
        elif tmp_attr.startswith('gene_biotype'):
            new_attrs.append('gene_type=%s' %
                             (tmp_attr.split('=')[1]))

            if tmp_attr.find('protein_coding') >= 0:
                is_protein_coding = 1
            if tmp_attr.find('pseudogene') >= 0:
                is_pseudogene = 1
            if tmp_attr.lower().find('rna') >= 0:
                is_rna= 1

    new_attrs.append('level=3')

    new_attr_str = ';'.join(new_attrs)

    #if is_rna == 0 and is_protein_coding == 0 and is_pseudogene == 0:
    #if is_rna > 0:
    #if is_pseudogene > 0:
    if is_protein_coding > 0:
        print("%s\t%s\t%s" % (tmp_chr_id, "\t".join(tokens[1:-2]), new_attr_str))
f_gff.close()
