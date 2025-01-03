# -*- coding: utf-8 -*-
"""Cybersecurity DDOS Final Project UTD

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YQS7ByCMGUD0EMEGyIOU3rTrjKzfkZ42
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
# %matplotlib inline

df = pd.read_csv('ddos_train-updated.csv')

df.head()

duration_concurrent = df[['Duration', 'Concurrent_Flow_Count']]

duration_concurrent.head()

km = KMeans(n_clusters=2, init='k-means++', random_state=None)
print(km)

from sklearn.mixture import GaussianMixture
gm = GaussianMixture(n_components=2)
print(gm)

plt.scatter(duration_concurrent['Duration'], duration_concurrent['Concurrent_Flow_Count'])
plt.show

from sklearn import cluster
dfpredict = km.fit_predict(duration_concurrent)

print(dfpredict)

duration_concurrent['cluster'] = dfpredict
dfpredict

test1 = pd.read_csv("ddos-test-1updated.csv")
test1.head()

labelA = test1['A']
labelA.head()

test1fr = test1[['Port', 'duration', 'Bi_pct', 'Up_pct', 'Down_pct', 'Tot_byt', 'H', 'I', 'Con_count']]
test1fr.head()

test1wdnc = test1[['duration', 'Con_count']]
test1.head()

test1predict = km.predict(test1wdnc)

print(test1predict)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import PrecisionRecallDisplay
cm = confusion_matrix(test1predict, labelA)
ac_score = accuracy_score(test1predict, labelA)
print(cm)
print(ac_score)

from sklearn.metrics import classification_report
print(classification_report(test1predict, labelA))

validation = pd.read_csv("validationset.csv")
validation.head()

validationprediction = km.predict(validation)

validationprediction

import seaborn as sns
import matplotlib.pyplot as plt
sns.scatterplot(data=test1, x='duration', y='Concurrent_Flow_Count', hue=test1predict)
plt.show()

test2 = pd.read_csv("ddos_test2real.csv")
test2.head()

labelAtest2 = test2['A']

labelAtest2.head()

test3 = test2[['Duration', 'Concurrent_Flow_count']]
test2.head()

clustertest2_predict = km.predict(test3)
clustertest2_predict

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import PrecisionRecallDisplay
cm = confusion_matrix(labelAtest2, clustertest2_predict)
ac_score = accuracy_score(labelAtest2, clustertest2_predict)
print(cm)
print(ac_score)

from sklearn.metrics import classification_report
print(classification_report(labelAtest2, clustertest2_predict))

benignsum = 0

length = len(labelAtest2)
lengthy = len(clustertest2_predict)


print(length)
print(lengthy)

benignsum = 0

for i in range(len(labelAtest2)):
  if labelAtest2.iloc[i] == 0 and clustertest2_predict.iloc[i] == 0:
    benignsum = benignsum + 1


print(benignsum)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import PrecisionRecallDisplay
cm = confusion_matrix(labelAtest2, clustertest2_predict)
ac_score = accuracy_score(labelAtest2, clustertest2_predict)
print(cm)
print(ac_score)

from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.metrics import make_scorer, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.mixture import GaussianMixture

isof = IsolationForest(random_state=0)

param_grid = {'contamination': [0.067]}

f1sc = make_scorer(f1_score, average='micro')
grid = GridSearchCV(isof, param_grid, scoring=f1sc, refit = True, n_jobs=-1)

grid.fit(df.values)
y_test = grid.best_estimator_.predict(test1fr)

print(confusion_matrix(test1["A"], y_test))
print(classification_report(test1["A"], y_test))

fpositive = 0
fnegative = 0
tpositive = 0
tnegative = 0

for i in range(len(y_test)):
    if test2["A"].iloc[i] == 0 and y_test[i] == -1: #0 = benign, 1 = ddos --> -1 = outlier, 1 = inlier, outliers are set as benign
        tnegative += 1
    elif test2["A"].iloc[i] == 1 and y_test[i] == -1:
        fnegative += 1
    elif test2["A"].iloc[i] == 1 and y_test[i] == 1:
        tpositive += 1
    elif test2["A"].iloc[i] == 0 and y_test[i] == 1:
        fpositive += 1

print(tnegative, fpositive, fnegative, tpositive)
print("Accuracy = " + str((tpositive+tnegative)/(tpositive+tnegative+fpositive+fnegative)))
print("Precision = " + str((tpositive)/(tpositive+fpositive)))
print("Recall = " + str((tpositive)/(tpositive+fnegative)))
print("F-score = " + str((tpositive)/(tpositive+(fpositive+fnegative)/2)))

print(grid.best_params_)

import numpy as np
from sklearn.decomposition import PCA
pca = PCA(2)
pca.fit(test2[['Duration', 'Concurrent_Flow_count']])
res=pd.DataFrame(pca.transform(test1fr))
Z = np.array(res)
plt.title("IsolationForest")
plt.contourf( Z, cmap=plt.cm.Blues_r)
b1 = plt.scatter(res[0], res[1], c='green',
                 s=20,label="normal points")
b1 =plt.scatter(res.iloc[outlier_index,0],res.iloc[outlier_index,1], c='green',s=20,  edgecolor="red",label="predicted outliers")
plt.legend(loc="upper right")
plt.show()