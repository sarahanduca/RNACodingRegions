# Main ===================================================================================================================
# Libraries and importations ===========================
import pickle   # Used for file operations
# Metrics is used to generate the final statistics on the trained model
from sklearn_crfsuite import metrics

# This import allows us to have a report of cross-validation results
from sklearn.model_selection import cross_val_predict
# ======================================================

# Input & output filenames (you can edit)
model_filename_input = "model_filename_output"
mod3_filename_input = "mod3_filename_output"

# Load the model to be tested
file = open("../results/"+model_filename_input+".sav", "rb")
clf = pickle.load(file)

# Load the data from module 3. Use the data corresponding to the model
file = open("../assets/mod3/"+mod3_filename_input+".mod3", "rb")
data = pickle.load(file)
samples = data[0]
labels = data[1]

# Cross-validate prediction. Results are printed on the console
pred = cross_val_predict(clf, samples, labels, cv=10)
print("Classification Report:")
x = ["Intron", "Exon"]
metrics.flat_f1_score(labels, pred, average="weighted", labels=x)
sorted_labels = sorted(x, key=lambda name: (name[1:], name[0]))
print(metrics.flat_classification_report(labels, pred, labels=sorted_labels, digits=2))
# ========================================================================================================================