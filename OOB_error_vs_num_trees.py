import matplotlib as mpl 
mpl.use("Agg")
import matplotlib.pyplot as plt
from collections import OrderedDict
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


print("Reading in the data...\n")
#Read in the gene expression data
X = pd.read_table("GDC_gene_expression_table.tsv", sep="\t", header=0, index_col=0)

#Read in the sample classes
y = pd.read_table("GDC_sample_cancer_type.tsv", sep="\t", header=None, index_col=0, names=["Cancer_type"])
#Reorder the rows to match up with the gene counts dataframe
y = y.reindex(X.index.values.tolist())

#Set random state for reproducibility of results
RANDOM_STATE = 123

rf = RandomForestClassifier(n_estimators=1000, warm_start=True, oob_score=True, random_state=RANDOM_STATE)

num_trees = [50, 100, 200, 350, 500, 750, 1000, 1500, 2000, 3000, 4000, 5000]
error_rate = OrderedDict()
#Train a random forest with various number of trees and record the out-of-bag (OOB) 
#error rate to validate the model
for trees in num_trees:

	print("Training random forest of %s trees..." % trees)
	#Train random forest
	rf.set_params(n_estimators=trees)
	rf.fit(X, y["Cancer_type"].values)

	#Record OOB error
	oob = 1 - rf.oob_score_
	error_rate[trees] = oob
	
	print("Number of trees: %s\t\tOOB error: %s\n" % (trees, oob))


#Plot OOB error rate vs number of trees
plt.figure()
plt.plot(error_rate.keys(), error_rate.values())
plt.xlabel("Number of trees")
plt.ylabel("OOB error rate")
plt.savefig("oob_error_rate_vs_num_trees.pdf")




	
	
