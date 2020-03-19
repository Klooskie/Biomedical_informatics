from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

float_formatter = lambda x: "%.2f" % x
np.set_printoptions(formatter={'float_kind': float_formatter})

X = [[10, 15], [12, 14], [13, 15], [12, 17], [13, 19],
     [20, 31], [19, 27], [21, 25], [20, 29], [22, 26]]  # features
y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]  # labels

X = np.asarray(X)
y = np.asarray(y)

clf = svm.SVC(kernel='rbf', gamma='auto')
scores = cross_val_score(clf, X, y, cv=5)
acc = scores.mean()
print('acc: {0:.2f}'.format(acc))

plt.plot(X[:, 0], X[:, 1], '*')
plt.show()

dataset = pd.read_csv('processed.cleveland.data', header=None)
rows_to_remove = np.array((dataset == '?').any(axis=1))
dataset = dataset[rows_to_remove == False]
X = np.asarray(dataset.iloc[:, :-1]).astype('float32')
y = np.asarray(dataset.iloc[:, -1]).astype('int32')

classifier = svm.SVC(kernel='rbf', gamma='auto')
scores = cross_val_score(classifier, X, y, cv=5)
acc = scores.mean()
print('SVC acc: {0:.2f}'.format(acc))

classifier = RandomForestClassifier()
scores = cross_val_score(classifier, X, y, cv=5)
acc = scores.mean()
print('RandomForestClassifier acc: {0:.2f}'.format(acc))

classifier = RandomForestClassifier(n_estimators=150, min_samples_leaf=4, bootstrap=False)
scores = cross_val_score(classifier, X, y, cv=5)
acc = scores.mean()
print('RandomForestClassifier tweaked acc: {0:.2f}'.format(acc))
