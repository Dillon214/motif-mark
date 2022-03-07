import re
import cairo
import argparse
import random

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
    "W":"[A,T,U]",
    "S":"[C,G]",
    "M":"[A,C]",
    "K":"[G,T,U]",
    "P":"[A,G]",
    "Y":"[C,T,U]",
    "B":"[G,C,T,U]",
    "D":"[A,G,T,U]",
    "H":"[A,C,T,U]",
    "V":"[A,G,C]",
    "N":"[A,G,C,T,U]",
    "A":"A",
    "C":"C",
    "T":"[T,U]",
    "G":"G",
    "U":"[U,T]"
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
        pattern = motif_search_seq
        
        
        #self.associated_motifs[motif_object_name] = tuple(m.start(), m.end()) for m in re.finditer(r'(?=(' + pattern + '))' ,(self.seq).upper()))
        iterable = re.finditer(r'(?=(' + pattern + '))' ,(self.seq).upper())
        self.associated_motifs[motif_object_name] = [(m.start(), m.start()+ len(motif_object_name)) for m in iterable]
        
            
        

        

class cairo_image:
    def __init__(self, name):
        self.name = name
        self.motif_colors = {}
    
    def draw_objects(self, seq_objects):
        global_yshift = 100
        global_xshift = 20
        
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, max((len(x.seq) for x in seq_objects)) + 300, 200*len(seq_objects))
        ctx = cairo.Context(surface)
        
        
        for i, seq_obj in enumerate(seq_objects):
            ctx.set_source_rgb(0.8,0.8,0.8)
            
            ctx.set_line_width(2)
            ctx.move_to(global_xshift,200*i + global_yshift)
            ctx.line_to(global_xshift + len(seq_obj.seq),200*i + global_yshift)
            ctx.move_to(global_xshift,200*i + global_yshift - 58)
            ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(14)
            
            ctx.show_text(seq_obj.name)
            ctx.stroke()

            
            
            

            num_motifs = len(seq_obj.associated_motifs)
            
            top_bound = 200*i + global_yshift - 50
            length = 100/(num_motifs + 0.01)

            for motifnum, x in enumerate(seq_obj.associated_motifs):
                
                if x not in self.motif_colors:
                    self.motif_colors[x] = (random.random(), random.random(), random.random())
                color = self.motif_colors[x]

                ctx.set_source_rgb(color[0], color[1], color[2])
                #ctx.set_source_rgb(0.6, 0.6, 0.6)
                vert = top_bound + length*motifnum


                motif_positions = seq_obj.associated_motifs[x]
                
                overlap = 1
                overlapstart = None
                for i, z in enumerate(motif_positions):
                    
                    if i > 0:
                        if z[0] < motif_positions[i - 1][1]:
                            overlap += 1
                        else:
                            if overlap > 1:
                                ctx.set_source_rgb(color[0], color[1], color[2])
                                ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                                ctx.set_font_size(13)
                                ctx.move_to(overlapstart + global_xshift, vert)
                                ctx.show_text("overlap")
                                ctx.stroke()
                                overlap = 1
                            overlapstart = z[0]
                    else:
                        overlapstart = z[0]

                

                    ctx.rectangle(z[0] + global_xshift, vert, z[1] - z[0], length)
                    ctx.fill()
                    ctx.stroke()
                
                #ctx.fill()
                #ctx.stroke()
                

                ctx.set_source_rgb(1,1,1)
                for z in motif_positions:
                    
                    ctx.rectangle(z[0] + global_xshift, vert, 0.7, length)

                ctx.fill()
                ctx.stroke()


                ctx.set_source_rgb(color[0], color[1], color[2])
        
                ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                ctx.set_font_size(13)
                ctx.move_to(30 + len(seq_obj.seq), vert + 15)
                ctx.show_text(x)

                ctx.set_source_rgb(0,0,0)

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





for seq_ob in seq_objects:
    for moti in motif_objects:
        seq_ob.find_motif_occurences(moti.motif, moti.searchpattern)


cairo_obj = cairo_image("booba")
cairo_obj.draw_objects(seq_objects)

