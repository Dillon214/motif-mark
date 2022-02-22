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

print("running")
seq_lines = fasta_file.readlines()
motif_lines = motif_file.readlines()

degendict = {
    "W":"[A,T]",
    "S":"[C,G]",
    "M":"[A,C]",
    "K":"[G,T]",
    "P":"[A,G]",
    "Y":"[C,T]",
    "B":"[G,C,T]",
    "D":"[A,G,T]",
    "H":"[A,C,T]",
    "V":"[A,G,C]",
    "N":"[A,G,C,T]",
    "A":"A",
    "C":"C",
    "T":"T",
    "G":"G",
    "U":"U"
}

def translatedegenerate(string):
    return "".join([degendict[x] for x in string])



class seq:
    def __init__(self, name, sequence):
        self.name = name
        self.seq = sequence
        self.associated_motifs = {}
        self.exon_locs = re.compile("[A-Z]").finditer((self.seq).upper())
        
        
        

    def find_motif_occurences(self, motif_object_name, motif_search_seq):
        p = re.compile(motif_search_seq)
        self.associated_motifs[motif_object_name] = tuple((m.start(), m.end()) for m in p.finditer((self.seq).upper()))
        

class cairo_image:
    def __init__(self, name):
        self.name = name
    
    def draw_objects(self, seq_objects):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, max((len(x.seq) for x in seq_objects)), 200*len(seq_objects) + 50)
        ctx = cairo.Context(surface)
        
        for i, seq_obj in enumerate(seq_objects):
            print(len(seq_obj.seq))
            ctx.set_line_width(2)
            ctx.move_to(20,200*i + 20)
            ctx.line_to(20 + len(seq_obj.seq),200*i + 20)
            ctx.stroke()
        surface.write_to_png("festi.png")

             
        

class motif:
    def __init__(self, motif):
        self.motif = motif
        self.searchpattern = translatedegenerate(self.motif.upper())
    
        

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


seq_objects[2].find_motif_occurences(motif_objects[0].motif, motif_objects[0].searchpattern)

cairo_obj = cairo_image("booba")
cairo_obj.draw_objects(seq_objects)
