import glob
from Bio import SeqIO
from Bio.SeqUtils import MeltingTemp as mt
import argparse
import distance
import time


files = glob.glob("./25mer_results/*.fasta")
seqs = SeqIO.parse("*.fasta", "fasta") #input fasta file of sequences here



def main(species_arg):
	
	unique_dict = {}
	for file in files:
		seq_dict = {}
		for item in files:
			if item !=file:
				for kmer in (SeqIO.parse(item, "fasta")):
					seq_dict.update({str(kmer.id): str(kmer.seq)})
		species_dict = {}
		for species_kmer in (SeqIO.parse(file, "fasta")):
			seq_target = species_kmer.seq[7:25]
			complement = seq_target.reverse_complement()
			cond1 = mt.Tm_NN(complement, nn_table= mt.R_DNA_NN1, Na=500, dnac1 = 100)
			cond2 = mt.Tm_NN(complement, nn_table= mt.R_DNA_NN1, dnac1= 13, Tris = 50, Mg =10)
			if cond1>55 and cond2>55:
				species_dict.update({str(species_kmer.id): str(species_kmer.seq)})
		seq_set = set(seq_dict.values())
		species_set = set(species_dict.values())
		unique_set = species_set - seq_set
		for sequence in unique_set:
			for key, value in species_dict.items():
				if sequence ==value:
					unique_dict.update({key: value})
	
	ref_dict = SeqIO.to_dict(seqs)
	for key, seq_record in ref_dict.items():
		seq_record = str(seq_record.seq)
		ref_dict[key] = seq_record
	
	new_unique_dict = {}
	
	specific = {}
	print(species_arg)
	
	for key, value in unique_dict.items():
		species = key[0:key.find("-")]
		if species==species_arg:
			specific[key] = value
	print(len(specific))
	for k, v in specific.items():
		count = 0
		start = time.time()
		species = k.split('-')[0]
		print(species)
		isMatch = False
		for name, nucleotides in ref_dict.items():
			if isMatch == True:
				break
			if name != species:
				for n in range(0,len(nucleotides)):
					#if isMatch:
					#	break
					target = nucleotides[n:n+25]
					if distance.levenshtein(v, target) <= 3:
						isMatch = True
						break
					stop = time.time()
					#print(stop-start)
					count +=1
					#print(count)
		print(count)
		if isMatch==False:
			new_unique_dict[k] = v
	print(len(new_unique_dict))
	results_file = open("./25mer_results/{}_results.fasta".format(species_arg, "w"))
	for key, value in new_unique_dict.items():
		results_file.write('>{}\n{}\n'.format(key, value))
	results_file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("species_arg", type=str, help="What taxa kmer do you want to use?")
	args = parser.parse_args()
	main(args.species_arg)




