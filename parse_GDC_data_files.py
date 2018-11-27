#Parse the gene expression (transcriptome profiling) text files for all 11,571 samples
#from the National Cancer Institute GDC Data Portal and combine it into a dataframe
#with rows as the samples and columns as the genes
#The gene expression data for these samples can be downloaded from:
#(https://portal.gdc.cancer.gov/repository?filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.analysis.workflow_type%22%2C%22value%22%3A%5B%22HTSeq%20-%20FPKM%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_type%22%2C%22value%22%3A%5B%22Gene%20Expression%20Quantification%22%5D%7D%7D%5D%7D)

import argparse
import json
import os
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("GDC_dir", help="Filpath to directory with the downloaded gene expression data files")
parser.add_argument("metadata", help="JSON metadata file from GDC with info about samples") 
args = parser.parse_args()


#Read in the sample metadata file
metadata = {}
with open(args.metadata, "r") as fin:
	data = json.load(fin)
for d in data:
	filename = d['file_name'] #Name of the expression data text file (This is unique for every sample, we'll use these as sample identifiers)
	case_id = d['cases'][0]['case_id'] #Identifier for the case (There are multiple samples for some case numbers)
	project_id = d['cases'][0]['project']['project_id'] #This ID lets us know which cancer type
	metadata[filename] = {}
	metadata[filename]['case_id'] = case_id
	metadata[filename]['project_id'] = project_id

#Dataframe to hold gene expression data for all samples
df_all = pd.DataFrame()
#Dictionary to keep track of sample cancer type (project id)
sample_cancer_type = {}

#Get list of all the downloaded data directories (each gene
#expression text file is in its own directory)
dirs = os.listdir(args.GDC_dir)

#Read each gene expression text file into a pandas dataframe, then
#join it into the aggregate dataframe based on the gene identifier (index)
for d in dirs:
	f = [i for i in os.listdir("/".join([args.GDC_dir, d])) if ".FPKM.txt" in i][0]
	sample_id = f.split("/")[-1].split(".")[0]
	proj_id = metadata[f]['project_id']
	sample_cancer_type[sample_id] = proj_id
	df_i = pd.read_table("/".join([args.GDC_dir, d, f]), sep="\t", header=None, names=["gene_id", sample_id], index_col=0)
	df_all = df_all.join(df_i, how="outer")

#Transpose the dataframe to get samples as rows and genes as columns
df_all = df_all.transpose()

#Save the dataframe to a tab-delimited text file
df_all.to_csv("GDC_gene_expression_table.tsv", sep="\t")
print("There are %s samples and %s genes" %(df_all.shape[0], df_all.shape[1]))

#Write sample cancer types to tab-delimited text file
with open("GDC_sample_cancer_type.tsv", "w") as fout:
	for tup in sample_cancer_type.iteritems():
		fout.write("\t".join(tup) + "\n")
