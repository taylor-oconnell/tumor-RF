import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import pickle

#Read in the gene expression data
X = pd.read_table("GDC_gene_expression_table.tsv", sep="\t", header=0, index_col=0)

#Read in the sample classes
y = pd.read_table("GDC_sample_cancer_type.tsv", sep="\t", header=None, index_col=0, names=["Cancer_type"])
#Reorder the rows to match up with the gene counts dataframe
y = y.reindex(X.index.values.tolist())

#Create and train random forest on the data
rf = RandomForestClassifier(n_estimators=1000, oob_score=True, n_jobs=40)
cv_results = cross_validate(rf,  X, y["Cancer_type"].values, cv=5, return_train_score=False, 
			    scoring=('accuracy', 'balanced_accuracy', 'f1_micro', 'f1_weighted'),
			    return_estimator=True)

#Save the cross-validation results as pickle file
pickle.dump(cv_results, open("random_forest_cross-validation_results.p", "wb"))

#Print out the results for each of the 5 random forest classifiers trained
#in the cross-validation
for i in range(5):
	print("/nRandom Forest %s" % (i+1))
	print("\tAccuracy: %s" % cv_results['test_accuracy'][i])
	print("\tBalanced Accuracy: %s" % cv_results['test_balanced_accuracy'][i])
	print("\tf1 score micro-averaged: %s" % cv_results['test_f1_micro'][i])
	print("\tf1 score weighted: %s" % cv_results['test_f1_weighted'][i])
	print("\tOOB error rate: %s" % (1 - cv_results['estimator'][i].oob_score_))

