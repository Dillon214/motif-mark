import re
import cairo
import argparse


parser = argparse.ArgumentParser(description='Import motifs and fasta.')
parser.add_argument('-m', help='motifs')
parser.add_argument('-f', help='fasta')

args = parser.parse_args()


fasta = args.f
motif = args.m

fasta_file = open(fasta, "r")

for line in fasta_file:
    print(line)