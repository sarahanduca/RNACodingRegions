# Main ===================================================================================================================
# Libraries and importations ===========================
import pickle               # Used for file operations
from sklearn_crfsuite import CRF     # Contains the functions to train, test and make predictions with the model
import random               # Used to generate random numbers
from sklearn_crfsuite import metrics

# This import allows us to have a report of cross-validation results
from sklearn.model_selection import cross_val_predict
# ======================================================

# Input & output filenames (you can edit)
mod2_filename_input = "mod2_filename_output"
mod3_filename_output = "mod3_filename_output"
model_filename_output = "model_filename_output"

# File generated in the previous module
file = open("../assets/mod2/"+mod2_filename_input+".mod2", "rb")
data = pickle.load(file)

# Samples is the variable that will contain all the sequences to be analyzed, according to the CRF input specification ([{"sequence": "..."}])
samples = []

# Labels is the variable that will contain all the sequences answers, for example, for samples[0], labels[0] can be or "Exon", or "Intron" or "Neither"
labels = []

# The aux is the variable that will contain all the sequences of "Neither"
aux = []

# The data[0] are all Exon sequences obtained in the last module. It is stored in the exons variable
exons = data[0]

# The data[1] are all Intron sequences obtained in the last module. It is stored in the introns variable
introns = data[1]

# Exon counter found
exonsCount = 0

# Intron counter found
intronsCount = 0

# While controller
i=0
while(i < len(exons)):                              # len(exons) = len(introns) = number of sequences obtained previously
    for seq in exons[i]:                            # for each subsequence in exons
        if(seq[-1] != "Neither"):                   # if the subsequence is not a "Neither" one
            samples.append([{"sequence":seq[0]}])   # the sequence is appended to samples
            labels.append([seq[-1]])                # the sequence is appended to labels
            exonsCount += 1                         # exon counter is incremented
        # else:
        #     aux.append([seq[0]])                    # The subsequence is a "Neither" one and it"s appended to aux

    for seq in introns[i]:                          # for each subsequence in introns
        if(seq[-1] != "Neither"):                   # if the subsequence is not a "Neither" one
            samples.append([{"sequence":seq[0]}])   # the sequence is appended to samples
            labels.append([seq[-1]])                # the sequence is appended to labels
            intronsCount += 1                       # intron counter is incremented
        # else:
        #     aux.append([seq[0]])                    # The subsequence is a "Neither" one and it"s appended to aux
    i+=1

# To balance the amount of "Neither" in the base, the average between exons and introns is calculated
# average = (exonsCount + intronsCount)/2

# For the average number of times, take a random aux element and append it to samples, putting "Neither" in labels
# for i in range(0,int(average)):
#     randomNumber = random.randint(0,len(aux)-1)
#     samples.append([{"sequence":aux[randomNumber][0]}])
#     # labels.append(["Neither"])
#     aux.pop(randomNumber)

# Instance the CRF algorithm
clf = CRF()

# Train the model
clf = clf.fit(samples, labels)
pred = cross_val_predict(clf, samples, labels, cv=10)
print("Classification Report:")
x = ["Intron", "Exon"]
metrics.flat_f1_score(labels, pred, average="weighted", labels=x)
sorted_labels = sorted(x, key=lambda name: (name[1:], name[0]))
print(metrics.flat_classification_report(labels, pred, labels=sorted_labels, digits=2))
# Saves the trained model (you can edit the file name)
pickle.dump(clf, open("../results/"+model_filename_output+".sav", "wb"))

# Saves the samples e labels
file = open("../assets/mod3/"+mod3_filename_output+".mod3","wb")
pickle.dump([samples,labels],file)
# ========================================================================================================================