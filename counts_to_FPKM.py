import pandas as pd


#Read the gene counts into pandas dataframe
counts = pd.read_table("htseq-count_gene_counts.txt", sep="\t", comment='_', header=None, names=["Count"], index_col=0)

#Parse the gtf file to get the length of the genes
#We're computing gene length as sum of the length of all exons 
#for the gene
gene_len = {}
with open("gencode.v22.annotation.gtf", "r") as fin:
	for line in fin:
		#Skip header/comment lines
		if line.startswith("##"):
			continue
		line = line.strip().split("\t")
		#Only look at the lines for the exons
		if line[2] != "exon":
			continue
		id = line[8].split(";")[0].split(" ")[1].replace('"','')
		#Exon length is end position minus start position
		length = int(line[4]) - int(line[3])
		if id not in gene_len:
			#First exon we find for the gene
			gene_len[id] = length
		else:
			#Additional exons; add to the length we have recorded so far
			gene_len[id] += length

#Convert gene lengths to dataframe
gene_len_df = pd.DataFrame.from_dict(gene_len, orient="index")
#Reorder the rows to match up with the gene counts dataframe
gene_len_df = gene_len_df.reindex(counts.index.values.tolist())

#Normalize the counts to FPKM
#Get total number of mapped reads
total_mapped = counts['Count'].sum()
#Calculate FPKM as: (num_reads_mapped_to_gene / (gene_length * total_mapped_reads)) * 10^9
fpkm = counts.multiply(1e09).iloc[:,0].divide(gene_len_df.multiply(total_mapped).iloc[:,0], axis=0)

#Write fpkm data to tab-separated text file
fpkm.to_csv('biopsy-A_fpkm.tsv', sep='\t')

