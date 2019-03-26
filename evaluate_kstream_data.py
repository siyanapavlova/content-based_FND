import pandas as pd
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn import svm
from matplotlib import pyplot as plt
import numpy

#One-time use code for training a SVC classifier on the Knowledge Stream test data
#Outputs accuracy, precision, recall and F-measure
#File can be replaced with 'scores_file_avg.csv' to get results for the average function
df = pd.read_csv('scores_file_max.csv', names=['score','class'])
clf = svm.SVC()
train, test = train_test_split(df, test_size=0.2)
clf.fit(train[['score']], train[['class']])
result = numpy.zeros([149, 2])

count = 0
for item in test['class']:
	result[count][0] = item
	count += 1

count = 0
for item in test['score']:
	result[count][1] = clf.predict(item)
	count += 1

true_positive = 0
true_negative = 0
false_positive = 0
false_negative = 0

for row in result:
	if row[1] == 0 and row[0] == 0:
		true_negative += 1
	if row[1] == 1 and row[0] == 1:
		true_positive += 1
	if row[1] == 1 and row[0] == 0:
		false_positive += 1
	if row[1] == 0 and row[0] == 1:
		false_negative += 1

print(df.shape)

n = 0
p = 0
for row in result:
	if row[0] == 0:
		n += 1
	else:
		p += 1

print("Positive/negative split of test set: %s/%s" % (p,n))

precision = true_positive/(true_positive+false_positive)
recall = true_positive/(true_positive+false_negative)
accuracy = (true_positive+true_negative)/(true_positive+true_negative+false_positive+false_negative)
f1_score = (2*precision*recall)/(precision+recall)

print("\n\nResults:\n\n")
print("Accuracy: "+str(accuracy))
print("\nPrecision: "+str(precision))
print("\nRecall: "+str(recall))
print("\nF-measure: "+str(f1_score))

print(test.shape)