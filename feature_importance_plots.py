import pickle
import sklearn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

#Load the cross-validation results pickle file output from the 
#GDC_random_forest_cross_validation.py script
cv_results = pickle.load(open('random_forest_cross-validation_results.p','rb'))

#Get feature importance values from each of the models
for i, model in enumerate(cv_results['estimator']):
	importances = model.feature_importances_
	indices = np.argsort(importances)[::-1]
	
	outname = "rf_%s_feature_importance" % (i+1) 
	#Plot feature importances
	plt.figure()
	plt.title("Feature importances")
	plt.xlabel("Feature")
	plt.ylabel("Importance (Gini)")
	plt.bar(range(len(importances)), importances[indices])
	plt.xlim([-1, len(importances)])
	plt.savefig(outname + ".pdf")

	#Write feature importance values to text file
	with open(outname + ".txt", "w") as fout:
		fout.write("Feature ranking:\n")
		for i in range(len(importances)):
			fout.write("%d. feature %d (%f)\n" % (i + 1, indices[i], importances[indices[i]]))



