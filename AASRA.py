#!/usr/bin/env python
##command line format: AASRA -f -p thread -i samplefile -l sampleAnchorSequence5' -r sampleAnchorSequence3' -b indexname
##command line example: AASRA -p 4 -i sample.fa -l CCCCC -r GGGGG -b anchored_index.fa

import argparse
import re
import sys

parser = argparse.ArgumentParser(prog='AASRA', usage='%(prog)s [-h] [-f] -p THREAD -i INPUT -l LEFTANCHORSEQ -r RIGHTANCHORSEQ -b BOWTIE2INDEX', description='Example: AASRA -p 4 -i sample.fa -l CCCCC -r GGGGG -b anchored_index.fa')
parser.add_argument('-p','--thread', help='Input the number of threads')
parser.add_argument('-f','--fasta', help='Specifiy if the input sample is fasta file')
parser.add_argument('-i','--input', help='Input file name, input file should be a fastq or fasta file.',required=True)
parser.add_argument('-l','--leftAnchorSeq',help='Input 5\' Anchor Sequence. Default left anchor sequence for reference index is CCCCC.', required=True)
parser.add_argument('-r','--rightAnchorSeq',help='Input 3\' Anchor Sequence. Default right anchor sequence for sample is GGGGG.', required=True)
parser.add_argument('-b','--bowtie2index',help='Input the name of pre-built bowtie2 index file.', required=True)
args = parser.parse_args()

##anchor sample
##open file##turn file into list of lines
with open(args.input,'r') as f_sample:
	line = f_sample.read().splitlines()
anchored_sample =open('anchored_' + args.input,'w')

adaptor5=args.leftAnchorSeq
adaptor3=args.rightAnchorSeq
quality5="I" * int(len(args.leftAnchorSeq))
quality3="I" * int(len(args.rightAnchorSeq))

#anchor fastq
##take out every 4 lines that begin with "@" and "+" for the 1st and third line, accordingly
a = 0

if line[a].startswith("@") and line[a+2].startswith("+") and a < 1:
	print ('\nInput sample is a fastq file. \n Anchor sequence is:' + '5\':' + adaptor5 + ', 3\':' + adaptor3 + '\n' + 'Generating anchored sample.')
	for line[a] in line:
		if line[a].startswith("@") and line[a+2].startswith("+"):
			anchored_sample.write(line[a]+ '\n')
			anchored_sample.write(adaptor5 + line[a+1] + adaptor3+ '\n')
			anchored_sample.write(line[a+2]+ '\n')
			anchored_sample.write(quality5 + line[a+3] + quality3+ '\n')
		a += 1
	print("\nsample anchored successfully\n")
##anchor fasta
elif line[a].startswith(">") and a < 1:
	print ('\nInput sample is a fasta file. Anchor sequence is:\n' + '5\':' + adaptor5 + ', 3\':' + adaptor3 + '\n' + 'Generating anchored sample.')
	a = 0
	for line[a] in line:
		if line[a].startswith(">"):
			anchored_sample.write(line[a]+ '\n')
			anchored_sample.write(adaptor5 + line[a+1] + adaptor3+ '\n')
		a += 1
	print("Sample anchored successfully.\n\nEntering alignment phase.")
else:
	print('\nInput sample is NOT a fasta/fastq file, please check the format of sample file.')

anchored_sample.close
