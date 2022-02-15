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
motif_file = open(motif, "r")


seq_lines = fasta_file.readlines()
motif_lines = motif_file.readlines()

degendict = {
    "W":"[A,T]",
    "S":"[C,G]",
    "M":"[A,C]",
    "K":"[G,T]",
    "P":"[A,G]",
    "B":"[G,C,T]",
    "D":"[A,G,T]",
    "H":"[A,C,T]",
    "V":"[A,G,C]",
    "N":"[A,G,C,T]"
}



def translatedegenerate(string):
    



class seq:
    def __init__(self, name, sequence):
        self.name = name
        self.seq = sequence
        self.searchpattern = 




class motif:
    def __init__(self, motif):
        self.motif = motif
    def searcher(self, seqobject):
        

linecounter = 0
linenames = []
lineseqs = []
making_lineseq = ""

for line in seq_lines:
    if line[0] == ">":
        if linecounter != 0:
            lineseqs.append(making_lineseq.strip())
            making_lineseq = ""
        linenames.append(line)
        linecounter+=1
        continue
    
    making_lineseq += line.strip()
lineseqs.append(making_lineseq)

seq_objects = [seq(linenames[num], lineseqs[num]) for num in range(linecounter)]

motif_objects = [motif(line.strip()) for line in motif_lines]


print(motif_objects[0].motif)


