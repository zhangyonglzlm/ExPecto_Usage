#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 12/3/2018 4:38 PM
# @Author  : Yong
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Help add REF and ALT columns')
parser.add_argument('inFile', type=str, action='store',
                    help='Path of the file without REF and ALT columns')

parser.add_argument('RefAlt', type=str, action='store',
                    help='Path of the file with REF and ALT information')

parser.add_argument('outFile', type=str, action='store',
                    help='Path of the file with REF and ALT columns')
args = parser.parse_args()

closestgene = pd.read_table(args.inFile, header=None, names=['CHROM', 'POS_0', 'POS', 'chr', 'TSS_0', 'TSS', 'Strand', 'Gene_ID', 'Dist'])
vcf = pd.read_table(args.RefAlt, header=None, names=['CHROM', 'POS', '-', 'REF', 'ALT'])

merged = pd.merge(closestgene, vcf, on=['CHROM', 'POS'], how='outer')
merged = merged.reindex(columns=['CHROM', 'POS_0', 'POS', 'REF', 'ALT', 'chr', 'TSS_0', 'TSS', 'Strand', 'Gene_ID', 'Dist'])
order_custom = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12',
                'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY']
merged['CHROM'] = merged['CHROM'].astype('category').cat.set_categories(order_custom)
merged.sort_values(by=['CHROM', 'POS'], ascending=True, inplace=True)

merged.to_csv(args.outFile, sep='\t', index=False, header=False)
