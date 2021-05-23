# -*- coding: utf-8 -*-
"""2 atribut klasifikasi

Automatically generated by Colaboratory.


https://colab.research.google.com/drive/1JJqbWiL_9DiV-ZeJYhwyIIKAI9yawQWG

#Tugas Besar Machine Learning



*   Nama : Andrea Rahmadanisya
*   NIM : 1301184146

*   Nama : Rizka Nur Octvaniani
*   NIM  : 1301184125

# Supervised

## Load Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import copy
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
#lib for model
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score as f1
from sklearn.metrics import accuracy_score as acc
from sklearn.metrics import precision_score as prec
from sklearn.metrics import recall_score as recall

DataTrain = pd.read_csv('kendaraan_train.csv')
DataTest = pd.read_csv('kendaraan_test.csv')

DataTrain = DataTrain.drop(["id"], axis=1)
DataTrain.head(3)

DataTrain["Tertarik"].value_counts()

"""## Clean Data Train"""

#fill NAN/missing value numerik using mean
DataTrain['Umur'].fillna(DataTrain['Umur'].mean(), inplace=True)
DataTrain['SIM'].fillna(DataTrain['SIM'].mean(), inplace=True)
DataTrain['Kode_Daerah'].fillna(DataTrain['Kode_Daerah'].mean(), inplace=True)
DataTrain['Sudah_Asuransi'].fillna(DataTrain['Sudah_Asuransi'].mean(), inplace=True)
DataTrain['Premi'].fillna(DataTrain['Premi'].mean(), inplace=True)
DataTrain['Kanal_Penjualan'].fillna(DataTrain['Kanal_Penjualan'].mean(), inplace=True)
DataTrain['Lama_Berlangganan'].fillna(DataTrain['Lama_Berlangganan'].mean(), inplace=True)
DataTrain['Tertarik'].fillna(DataTrain['Tertarik'].mean(), inplace=True)

#fill missing value categorical using modus
DataTrain['Jenis_Kelamin'].fillna('Pria', inplace=True)
DataTrain['Umur_Kendaraan'].fillna('1-2 Tahun', inplace=True)
DataTrain['Kendaraan_Rusak'].fillna('Pernah', inplace=True)

# len(DataTrain)
DataTrain.isna().sum()

DataTrain.info()

DataTrain['Jenis_Kelamin']= LabelEncoder().fit_transform(DataTrain['Jenis_Kelamin']) 
DataTrain['Umur_Kendaraan']= LabelEncoder().fit_transform(DataTrain['Umur_Kendaraan']) 
# Train['Kendaraan_Rusak']= LabelEncoder().fit_transform(Train['Kendaraan_Rusak']) 

# Train['Jenis_Kelamin'] = (Train['Jenis_Kelamin']=='Pernah').astype(int)
# Train['Umur_Kendaraan'] = (Train['Umur_Kendaraan']=='Pernah').astype(int)
DataTrain['Kendaraan_Rusak'] = (DataTrain['Kendaraan_Rusak']=='Pernah').astype(int)

DataTrain.head(3)

#check correlation
sns.set(rc={'figure.figsize':(11,8)})
def heatmap(data):
  sns.heatmap(data.corr(), vmax=1, annot=True, cmap='Pastel1')

heatmap(DataTrain)

#outlier
def Check_outlier(data):
  plt.figure(figsize=(60, 60))
  f, axes = plt.subplots(1, 9)
  sns.boxplot(y= data['Jenis_Kelamin'], ax= axes[0], color='rosybrown')
  sns.boxplot(y= data['Umur'], ax= axes[1], color='rosybrown')
  sns.boxplot(y= data['SIM'], ax=axes[2], color='rosybrown')
  sns.boxplot(y= data['Kode_Daerah'], ax=axes[3], color='rosybrown')
  sns.boxplot(y= data['Sudah_Asuransi'], ax=axes[4], color='rosybrown')
  sns.boxplot(y= data['Umur_Kendaraan'], ax=axes[5], color='rosybrown')
  sns.boxplot(y= data['Premi'], ax=axes[6], color='rosybrown')
  sns.boxplot(y= data['Kanal_Penjualan'], ax=axes[7], color='rosybrown')
  sns.boxplot(y= data['Lama_Berlangganan'], ax=axes[8], color='rosybrown')
  plt.subplots_adjust(wspace=0)

Check_outlier(DataTrain)

#handle outlier 
while True:
  qlo1, qlo3 = np.percentile(DataTrain['SIM'],[25,75])
  iqrlo = qlo3 - qlo1
  lowerlo = qlo1 - (1.5 * iqrlo)
  upperlo = qlo3 + (1.5 * iqrlo)
  outlierlo = DataTrain[(DataTrain['SIM'] < (lowerlo)) | (DataTrain['SIM'] > (upperlo))]
  print('amount of outlier data',outlierlo.shape[0]) #amount of outlier data
  idxlo = outlierlo.index
  DataTrain.drop(idxlo, inplace=True) #drop outlier data
  if (outlierlo.shape[0] <= 0):
    break

DataTrain['SIM'].describe()

#handle outlier 
while True:
  qlo1, qlo3 = np.percentile(DataTrain['Premi'],[25,75])
  iqrlo = qlo3 - qlo1
  lowerlo = qlo1 - (1.5 * iqrlo)
  upperlo = qlo3 + (1.5 * iqrlo)
  outlierlo = DataTrain[(DataTrain['Premi'] < (lowerlo)) | (DataTrain['Premi'] > (upperlo))]
  print('amount of outlier data',outlierlo.shape[0]) #amount of outlier data
  idxlo = outlierlo.index
  DataTrain.drop(idxlo, inplace=True) #drop outlier data
  if (outlierlo.shape[0] <= 0):
    break

DataTrain['Premi'].describe()

#handle outlier 
while True:
  qlo1, qlo3 = np.percentile(DataTrain['Lama_Berlangganan'],[25,75])
  iqrlo = qlo3 - qlo1
  lowerlo = qlo1 - (1.5 * iqrlo)
  upperlo = qlo3 + (1.5 * iqrlo)
  outlierlo = DataTrain[(DataTrain['Lama_Berlangganan'] < (lowerlo)) | (DataTrain['Lama_Berlangganan'] > (upperlo))]
  print('amount of outlier data',outlierlo.shape[0]) #amount of outlier data
  idxlo = outlierlo.index
  DataTrain.drop(idxlo, inplace=True) #drop outlier data
  if (outlierlo.shape[0] <= 0):
    break

DataTrain['Lama_Berlangganan'].describe()

#outlier
def Check_outlierdone(data):
  plt.figure(figsize=(60, 60))
  f, axes = plt.subplots(1, 9)
  sns.boxplot(y= data['Jenis_Kelamin'], ax= axes[0], color='rosybrown')
  sns.boxplot(y= data['Umur'], ax= axes[1], color='rosybrown')
  sns.boxplot(y= data['SIM'], ax=axes[2], color='rosybrown')
  sns.boxplot(y= data['Kode_Daerah'], ax=axes[3], color='rosybrown')
  sns.boxplot(y= data['Sudah_Asuransi'], ax=axes[4], color='rosybrown')
  sns.boxplot(y= data['Umur_Kendaraan'], ax=axes[5], color='rosybrown')
  sns.boxplot(y= data['Premi'], ax=axes[6], color='rosybrown')
  sns.boxplot(y= data['Kanal_Penjualan'], ax=axes[7], color='rosybrown')
  sns.boxplot(y= data['Lama_Berlangganan'], ax=axes[8], color='rosybrown')
  plt.subplots_adjust(wspace=0)

Check_outlierdone(DataTrain)

DataTest.fillna(DataTest.mean(), inplace=True)
DataTest.head(3)
DataTest.isna().sum()

DataTest['Jenis_Kelamin']= LabelEncoder().fit_transform(DataTest['Jenis_Kelamin']) 
DataTest['Umur_Kendaraan']= LabelEncoder().fit_transform(DataTest['Umur_Kendaraan']) 
# DataTest['Kendaraan_Rusak']= LabelEncoder().fit_transform(DataTest['Kendaraan_Rusak']) 

DataTest['Kendaraan_Rusak'] = (DataTest['Kendaraan_Rusak']=='Pernah').astype(int)

DataTest.head(3)

#check correlation
heatmap(DataTest)

#outlier
Check_outlier(DataTest)

#handle outlier 
while True:
  qlo1, qlo3 = np.percentile(DataTest['SIM'],[25,75])
  iqrlo = qlo3 - qlo1
  lowerlo = qlo1 - (1.5 * iqrlo)
  upperlo = qlo3 + (1.5 * iqrlo)
  outlierlo = DataTest[(DataTest['SIM'] < (lowerlo)) | (DataTest['SIM'] > (upperlo))]
  print('amount of outlier data',outlierlo.shape[0]) #amount of outlier data
  idxlo = outlierlo.index
  DataTest.drop(idxlo, inplace=True) #drop outlier data
  if (outlierlo.shape[0] <= 0):
    break

DataTest['SIM'].describe()

#handle outlier 
while True:
  qlo1, qlo3 = np.percentile(DataTest['Premi'],[25,75])
  iqrlo = qlo3 - qlo1
  lowerlo = qlo1 - (1.5 * iqrlo)
  upperlo = qlo3 + (1.5 * iqrlo)
  outlierlo = DataTest[(DataTest['Premi'] < (lowerlo)) | (DataTest['Premi'] > (upperlo))]
  print('amount of outlier data',outlierlo.shape[0]) #amount of outlier data
  idxlo = outlierlo.index
  DataTest.drop(idxlo, inplace=True) #drop outlier data
  if (outlierlo.shape[0] <= 0):
    break

DataTest['Premi'].describe()

#handle outlier 
while True:
  qlo1, qlo3 = np.percentile(DataTest['Umur'],[25,75])
  iqrlo = qlo3 - qlo1
  lowerlo = qlo1 - (1.5 * iqrlo)
  upperlo = qlo3 + (1.5 * iqrlo)
  outlierlo = DataTest[(DataTest['Umur'] < (lowerlo)) | (DataTest['Umur'] > (upperlo))]
  print('amount of outlier data',outlierlo.shape[0]) #amount of outlier data
  idxlo = outlierlo.index
  DataTest.drop(idxlo, inplace=True) #drop outlier data
  if (outlierlo.shape[0] <= 0):
    break

DataTest['Umur'].describe()

#outlier
def Check_outlier(data):
  plt.figure(figsize=(60, 60))
  f, axes = plt.subplots(1, 9)
  sns.boxplot(y= DataTest['Jenis_Kelamin'], ax= axes[0], color='rosybrown')
  sns.boxplot(y= DataTest['Umur'], ax= axes[1], color='rosybrown')
  sns.boxplot(y= DataTest['SIM'], ax=axes[2], color='rosybrown')
  sns.boxplot(y= DataTest['Kode_Daerah'], ax=axes[3], color='rosybrown')
  sns.boxplot(y= DataTest['Sudah_Asuransi'], ax=axes[4], color='rosybrown')
  sns.boxplot(y= DataTest['Umur_Kendaraan'], ax=axes[5], color='rosybrown')
  sns.boxplot(y= DataTest['Premi'], ax=axes[6], color='rosybrown')
  sns.boxplot(y= DataTest['Kanal_Penjualan'], ax=axes[7], color='rosybrown')
  sns.boxplot(y= DataTest['Lama_Berlangganan'], ax=axes[8], color='rosybrown')
  plt.subplots_adjust(wspace=0)

Check_outlier(DataTest)

"""## Pemodelan"""

DTrain = DataTrain[['Umur','Premi','Tertarik']]
DTrain.head()

targetTrain = DTrain['Tertarik']
Train = DTrain.drop(["Tertarik"], axis=1)
Train.head(3)

DTest = DataTest[['Umur','Premi','Tertarik']]
DTest.head()

targetTest = DTest['Tertarik']
Test = DTest.drop(['Tertarik'], axis=1)
Test.head(3)

print(targetTrain)
print(targetTest)

"""### Split data"""

Xtrain, ytrain = Train[:], targetTrain
Xtest, ytest = Test[:], targetTest

Xtrain = Xtrain.values
Xtest = Xtest.values
ytrain = ytrain.values
ytest = ytest.values

Xtrain

Xtest

ytrain

ytest

len(Xtest)

len(ytest)

"""### SVM"""

# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# import sklearn.metrics as metrics
svm = SVC()
svm.fit(Xtrain, ytrain)
SVM_pred = svm.predict(Xtest)
print("Support Vector Machine\n")
# for i in range(len(SVM_pred)):
#     print(SVM_pred[i])

print("F1-SCORE ",f1(ytest,SVM_pred,average='macro') * 100)

print("ACCURACY ",acc(ytest,SVM_pred) * 100)

print("PRECISION ",prec(ytest,SVM_pred,average='macro') * 100)

print("RECALL",recall(ytest,SVM_pred,average='macro') * 100)

TestEvalSVM = DTest.copy()
TestEvalSVM['Hasil Prediksi SVM'] = SVM_pred

TestEvalSVM.head()

"""### Evaluasi"""

from sklearn import metrics

def confusion_metrics (y_test,y_pred):
    #Showing Confusion Matrix to know True Positive, False Positive, True Negative and False Negative   
    cm = metrics.confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(cm, 
                         columns = ['Predicted Negative', 'Predicted Positive'], 
                         index = ['Actual Negative', 'Actual Positive'])

    #Assign True Positive, False Positive, True Negative and False Negative intu variable
    TN = cm_df.loc['Actual Negative','Predicted Negative']
    FN = cm_df.loc['Actual Positive','Predicted Negative']
    FP = cm_df.loc['Actual Negative','Predicted Positive']
    TP = cm_df.loc['Actual Positive','Predicted Positive']
    
    print('True Negative  : ',TN)
    print('False Negative : ',FN)
    print('False Positive : ',FP)
    print('True Positive  : ',TP)
    print('')
    
    #Find Precision, Recall, and F1-Score
    from sklearn.metrics import classification_report
    print(classification_report(y_test,y_pred))

#confusion Metrics
confusion_metrics(ytest,SVM_pred)

#Eksperimen
#Random Forest
rf = RandomForestClassifier().fit(Xtrain, ytrain)
# report.metrics(rf)
rf_predict = rf.predict(Xtest)

print("Random Forest\n")
# for i in range(len(cd_predict)):
#     print(cd_predict[i])

print("F1-SCORE ",f1(ytest,rf_predict,average='macro') * 100)
print("ACCURACY ",acc(ytest,rf_predict) * 100)
print("PRECISION ",prec(ytest,rf_predict,average='macro') * 100)
print("RECALL",recall(ytest,rf_predict,average='macro') * 100)

#evaluasi random forest
TestEvalRF = DTest.copy()
TestEvalRF['Hasil Prediksi RF'] = rf_predict

TestEvalRF.head()

#confusion Metrics Random Forest
confusion_metrics(ytest,rf_predict)

#Eksperimen KNN
#Create a KNeighbors Classifier
knn = KNeighborsClassifier(n_neighbors=5)

# Train the model using the training sets
knn.fit(Xtrain,ytrain)

#Predict Output
knn_predict = knn.predict(Xtest)

# Accuracy score
print("K NEAREST NEIGHBOR\n")
# for i in range(len(knn_predict)):
#     print(knn_predict[i])

print("F1-SCORE ",f1(ytest,knn_predict,average='macro') * 100)

print("ACCURACY ",acc(ytest,knn_predict) * 100)

print("PRECISION ",prec(ytest,knn_predict,average='macro') * 100)

print("RECALL",recall(ytest,knn_predict,average='macro') * 100)

#Perbandingan 
TestEvalKNN = DTest.copy()
TestEvalKNN['Hasil Prediksi KNN'] = knn_predict

TestEvalKNN.head()

#confusion Metrics KNN
confusion_metrics(ytest,knn_predict)
