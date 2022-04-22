import glob
from Bio import SeqIO
from Bio.SeqUtils import MeltingTemp as mt

#making 25mers
REFERENCE = "DeansEndoPhytoSeqs.fasta"
seqs = SeqIO.parse(REFERENCE, "fasta")
for seq_record in seqs:
	query_target=str(seq_record.id)
	nucleotides = str(seq_record.seq)
	kmer = 25
	results_file = open("./{}mer_results/{}.fasta".format(kmer, query_target), "w")
	for n in range(0,len(nucleotides)):
		target = nucleotides[n:n+kmer]
		if len(target)==kmer:
			results_file.write('>{}-{}\n{}\n'.format(query_target, n+1, target))
	results_file.close()