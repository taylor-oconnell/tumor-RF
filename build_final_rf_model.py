import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle


#Read in the gene expression data
X = pd.read_table("GDC_gene_expression_table.tsv", sep="\t", header=0, index_col=0)
#Read in the sample classes
y = pd.read_table("GDC_sample_cancer_type.tsv", sep="\t", header=None, index_col=0, names=["Cancer_type"])
#Reorder the rows to match up with the gene counts dataframe
y = y.reindex(X.index.values.tolist())

#Create and train random forest on the data
rf = RandomForestClassifier(n_estimators=1000, oob_score=True, n_jobs=-1)
rf.fit(X, y["Cancer_type"].values)

print("OOB error rate: " + str(1 - rf.oob_score_))

pickle.dump(rf, open('GDC_final_random_forest.p', 'wb'))




