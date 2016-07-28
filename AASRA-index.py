#!/usr/bin/env python
##command line format: AASRA-index indexfile indexAnchorSequence5' indexAnchorSequence3'
##command line example: AASRA-index -i index.fa -l CCCCCCCCCC -r GGGGGGGGGG -s index.saf
import argparse
import re
import sys

parser = argparse.ArgumentParser(prog='AASRA-index', usage='%(prog)s [-h] -i INPUT -l LEFTANCHORSEQ -r RIGHTANCHORSEQ -s SAF', description='Example: AASRA-index -i index.fa -l CCCCCCCCCC -r GGGGGGGGGG -s index.saf')
parser.add_argument('-i','--input', help='Input file name, input file should be a fasta file.',required=True)
parser.add_argument('-l','--leftAnchorSeq',help='Input 5\' Anchor Sequence. Default left anchor sequence for reference index is CCCCCCCCCC.', required=True)
parser.add_argument('-r','--rightAnchorSeq',help='Input 3\' Anchor Sequence. Default right anchor sequence for reference index is GGGGGGGGGG.', required=True)
parser.add_argument('-s','--saf', help='Input file name for the SAF file generate by AASRA-index, eg \'index.saf\'')
args = parser.parse_args()

if args.input:
	##anchor index
	with open(args.input,'r') as f_index:
		line = f_index.read().splitlines()
	anchored_index =open('anchored_' + args.input,'w')

	adaptor5=args.leftAnchorSeq
	adaptor3=args.rightAnchorSeq

	a = 0
	if line[a].startswith(">") and a < 1:
		print ('\nInput index is a fasta file. Anchor sequence is:\n' + '5\':' + adaptor5 + ', 3\':' + adaptor3 + '\n' + '\n' + 'Generating anchored index.')
		for line[a] in line:
			if line[a].startswith(">"):
				anchored_index.write(line[a]+ '\n')
				anchored_index.write(adaptor5 + line[a+1] + adaptor3+ '\n')
			a += 1
		print("Index anchored successfully.\n")
	else:
		print('\nInput index is NOT a fasta file, please check the format of index file.')
	anchored_index.close

	##generate SAF
	if args.saf:
		print('Generating ' + args.saf + '.')
		adaptor = adaptor5 + adaptor3
		saf_file =open(args.saf,'w')
		a = 0
		saf_file.write('GeneID' + '\t' +  'Chr'	 + '\t' + 'Start'  + '\t' + 'End'  + '\t' + 'Strand' + '\n')
		for line[a] in line:
			if line[a].startswith(">"):
				GeneID = re.findall('^>(.+)', line[a])
				seq_length = line[a+1] + adaptor
				saf_file.write(GeneID[0] + '\t' + GeneID[0] + '\t' + '1' + '\t' + str(len(seq_length)) + '\t' + '+' + '\n')
			a += 1
		print("SAF file generated successfully.\n")
		saf_file.close
