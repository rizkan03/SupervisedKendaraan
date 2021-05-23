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
