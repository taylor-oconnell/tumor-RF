import pandas as pd
import pickle
import sklearn

#Load the final random forest classifier
rf = pickle.load(open("GDC_final_random_forest.p", "rb"))
#Load the gene order
gene_order = []
with open("gene_order.txt", "r") as fin:
	for line in fin:
		gene_order.append(line.strip())

#Load the gene expression FPKM data for tumor sample
#to make prediction on
sample = pd.read_table("biopsy-A_fpkm.tsv", sep="\t", header=None, index_col=0)
#Reorder the gene expression fpkm values to match the order of the 
#inputs the random forest was trained on
sample = sample.reindex(gene_order)
sample = sample.transpose()

#Predict the class for the new sample
predicted_class = rf.predict(sample)
print("Predicted class / cancer type: %s" % predicted_class)

#Predict the probabilities for each class for the sample
predicted_probs = rf.predict_proba(sample)
classes = rf.classes_
for i in range(len(classes)):
	print(classes[i] + "\t" + str(predicted_probs[0][i]))


