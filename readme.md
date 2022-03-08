
motif-mark-oop.py takes in a motif file as input and a fasta file as input.
Produces a PNG format figure displaying to-scale motif occurances on fasta file sequences in working directory.
Exon locations, total motif occurances, and motif overlapping information are also displayed. . 

Arguments:\n
	-m path to motif file\n
	-f path to fasta file\n
	-o treat overlaps as one motif occurance\n

Note: overlapping instances of a given motif are treated as individual occurances by default, unless specified otherwise with the -o argument 


Example:
python motif-mark-oop.py -m fig1_motifs.txt -f fig1.fasta
