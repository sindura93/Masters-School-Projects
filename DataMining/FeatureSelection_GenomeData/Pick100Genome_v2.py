# -*- coding: utf-8 -*-
"""
Created on Sat May  5 00:27:52 2018

@author: sindu
About: Feature Selection on Genome Data"""

import pandas as pd
import numpy as np
import math
import operator
from sklearn import metrics
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import linear_model

filename = 'GenomeTrainXY.txt'
data = pd.read_csv('GenomeTrainXY.txt', header=-1).as_matrix()
testDataFile = "GenomeTestX.txt"
testData = pd.read_csv("GenomeTestX.txt", header=-1).as_matrix()
headerinfo = data[0]
classlabelinfo = list(set(headerinfo))
clbl, clblcnt = np.unique(headerinfo, return_counts=True)
classlabelcountinfo = dict(zip(clbl, clblcnt))
n_genomesize = len(headerinfo)
k_groupsize = len(clbl)
df = pd.DataFrame(data)
dftranspose = df.transpose()
fscores = pd.DataFrame()
fscorenumval = None
fscoredenom = None
fscorenumdf = pd.DataFrame()
fscoredenomdf = pd.DataFrame()

#calculate mean of all features for a specific class label
featuremeandata = df.transpose().groupby(dftranspose[:][0]).mean()
featuremeandata = featuremeandata.loc[:, 1:]
centroidData = featuremeandata.transpose().as_matrix()

#calculate variance of all features for a specific class label
featurevardata = df.transpose().groupby(dftranspose[:][0]).var()
featurevardata = featurevardata.loc[:, 1:]

#calculate average of each of the feature
featureavg = df.mean(axis=1)
featureavgdata = pd.DataFrame(featureavg).transpose()
featureavgdata = featureavgdata.loc[:, 1:]

def getfeaturemeandata(classlblval, val):
    meanrowdata = pd.DataFrame()
    meanrowdatabyvalue = pd.DataFrame()
    meannumdata = pd.DataFrame()
    for i in range(k_groupsize):
        if featuremeandata.index[i] == classlblval:
            meanrowdata = pd.DataFrame(featuremeandata.loc[classlblval, :]).transpose()
            meannumdata = meanrowdata.values - featureavgdata.values
            meanrowdatabyvalue = val*(pd.DataFrame((meannumdata)**2))
    return meanrowdatabyvalue

def getfeaturevardata(classlblval, val):
    varrowdata = pd.DataFrame()
    varrowdatabyvalue = pd.DataFrame()    
    for i in range(k_groupsize):
        if featurevardata.index[i] == classlblval:
            varrowdata = pd.DataFrame(featurevardata.loc[classlblval, :]).transpose()
            varrowdatabyvalue = pd.DataFrame(((val-1)*varrowdata))        
    return varrowdatabyvalue

# pick genome observations based on top 100 f-score
def pickGenome():
    for key, value in classlabelcountinfo.items():
        # constructing fscore numerator and denominator vector
        if list(classlabelcountinfo.keys()).index(key) == 0:
            fscorenumdf = getfeaturemeandata(key, value)
            fscoredenomdf = getfeaturevardata(key, value)
        else:
            testnumdf = getfeaturemeandata(key, value)
            testdenomdf = getfeaturevardata(key, value)
            fscorenumdf = pd.concat([fscorenumdf, testnumdf], axis=0, ignore_index=True)
            fscoredenomdf = pd.concat([fscoredenomdf, testdenomdf], axis=0, ignore_index=True)
    
        
    #print(fscorenumdf)
    #print(fscoredenomdf)    
        
    # calculating all the f-score numerator vector by summing mean data and dividing by k-1
    fscorenumdata = ((pd.DataFrame(fscorenumdf.sum(axis=0)).transpose())/(k_groupsize - 1))
    #print(fscorenumdata)
    
    # calculating all the f-score denominator vector by summing var data and dividing by n-k
    fscorevardata = ((pd.DataFrame(fscoredenomdf.sum(axis=0)).transpose())/(n_genomesize - k_groupsize))
    #print(fscorevardata)
    
    fscorenumdata.columns = range(fscorenumdata.shape[1])
    fscorevardata.columns = range(fscorevardata.shape[1])
    
    #calculating f-score
    fscores =  (fscorenumdata / fscorevardata).transpose()
    fscores.columns = ['Genome_fscore']
    #print(fscores)
    
    fscoreSorted = fscores.sort_values(by='Genome_fscore', ascending=False)
    print("========== Sorted fscores below ==============\n")
    print(fscoreSorted)
    
    top100fscoreindices = fscoreSorted.head(100).index.tolist()
    top100fscoreindices = [(x + 1) for x in top100fscoreindices]
    print("\n========== Top 100 fscore indices below ==============\n")
    print(top100fscoreindices)
    storeTop100GenomeData(top100fscoreindices)
    generateTop100TestData(top100fscoreindices)        

# from the observations that has top 100 f-score data, create and store the train data from those 100 observations
def storeTop100GenomeData(genomeList):
    file = open("GenomeTop100TrainData.txt", "w")
    r1, = data[0][:].shape
    rx,cx = data.shape
    for i in range(0, r1):
        file.write(str(int(data[0][:][i])))
        if (i < r1 - 1):
            file.write(',')
    file.write("\n")
    for a in genomeList:        
        for b in range(0, cx):
            file.write(str(data[a][:][b]))
            if(b < cx - 1):
                file.write(',')
        file.write("\n")
    file.close()

# from the observations that has top 100 f-score data, create and store the test data from those 100 observations
def generateTop100TestData(genomeList):
    file = open("GenomeTop100TestData.txt", "w")
    rx,cx = testData.shape
    for a in genomeList:        
        for b in range(0, cx):
            file.write(str(testData[a-1][:][b]))
            if(b < cx - 1):
                file.write(',')
        file.write("\n")
    file.close()

pickGenome()

# using the train and test samples created from the 100 observations that has top f-score, classify the data using various classification models
def data_classify(classifier):
    if (classifier == "KNN"):
        #storeData(Xtrain, ytrain, Xtest, ytest, classifier)
        file1 = pd.read_csv('GenomeTop100TrainData.txt', header=-1)
        Xtrain = file1.loc[1:,:].transpose().as_matrix()
        ytrain = file1.loc[0,:].transpose().as_matrix()
        file2 = pd.read_csv('GenomeTop100TestData.txt', header=-1)
        Xtest = file2.transpose().as_matrix()
        knneighbors = KNeighborsClassifier(n_neighbors=5)
        knneighbors.fit(Xtrain, ytrain)
        # calculating prediction
        predictions = knneighbors.predict(Xtest)
        # print(predictions)
        #actual = ytest
        #accuracy = metrics.accuracy_score(actual, predictions) * 100
        # printing accuracy
        #print("Accuracy with KNN =  ", accuracy)
        print('\n KNN Predictions: ', predictions)
        #accuracy = calc_accuracy(testData, predictions)
        #print('Accuracy with KNN =  ' + repr(accuracy) + '%')
    elif (classifier == "Centroid"):
        file1 = pd.read_csv('GenomeTop100TrainData.txt', header=-1)
        Xtrain = file1.loc[1:,:].transpose().as_matrix()
        ytrain = file1.loc[0,:].transpose().as_matrix()
        file2 = pd.read_csv('GenomeTop100TestData.txt', header=-1)
        Xtest = file2.transpose().as_matrix()
        centroid = NearestCentroid()
        centroid.fit(Xtrain, ytrain)
        # calculating prediction
        predictions = centroid.predict(Xtest)
        # printing accuracy
        #accuracy = metrics.accuracy_score(ytest, predictions) * 100
        #print("Accuracy with Centroid = ", accuracy)
        print('\n Centroid predictions: ', predictions)
        #accuracy = calc_accuracy(testData, predictions)
        #print('Accuracy with Centroid =  ' + repr(accuracy) + '%')
    elif (classifier == "SVM"):
        file1 = pd.read_csv('GenomeTop100TrainData.txt', header=-1)
        Xtrain = file1.loc[1:,:].transpose().as_matrix()
        ytrain = file1.loc[0,:].transpose().as_matrix()
        file2 = pd.read_csv('GenomeTop100TestData.txt', header=-1)
        Xtest = file2.transpose().as_matrix()
        svmclassifier = svm.LinearSVC()
        svmclassifier.fit(Xtrain, ytrain)
        # calculating prediction
        predictions = svmclassifier.predict(Xtest)
        print('\n SVM Predictions: ',predictions)
        #actual = ytest
        #accuracy = metrics.accuracy_score(actual, predictions) * 100
        # printing accuracy
        #print("Accuracy with SVM = ", accuracy , '%')
    elif(classifier == "Linear Regression"):
        file1 = pd.read_csv('GenomeTop100TrainData.txt', header=-1)
        Xtrain = file1.loc[1:,:].transpose().as_matrix()
        ytrain = file1.loc[0,:].transpose().as_matrix()
        file2 = pd.read_csv('GenomeTop100TestData.txt', header=-1)
        Xtest = file2.transpose().as_matrix()
        lm = linear_model.LinearRegression()
        lm.fit(Xtrain,ytrain)
        # calculating prediction
        predictions = lm.predict(Xtest)
        print('\n LR Predictions: ',predictions)
        # print(predictions)
        #actual = ytest
        #accuracy = metrics.r2_score(actual, predictions) * 100
        # printing accuracy
        #print("Accuracy with Linear Regression = ", accuracy)

y_knn = data_classify("KNN")
y_cent = data_classify("Centroid")
y_svm = data_classify("SVM")
y_lr = data_classify("Linear Regression")
