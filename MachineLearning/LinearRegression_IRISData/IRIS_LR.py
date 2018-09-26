# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 20:46:49 2018

@author: sindu
"""

import numpy as np
import pandas as pd
from sklearn.cross_validation import KFold
from sklearn import metrics
from sklearn.metrics import accuracy_score, mean_squared_error

# reading data 
data = pd.read_csv('IrisData.txt', header=-1).as_matrix()
#Separting class labels and observations
XVectorData = pd.DataFrame(data[:,0:4])
YData = data[:, -1]
YVectorData = []

ClassLabelNumerical = {'Iris-setosa':1, 'Iris-versicolor':2, 'Iris-virginica':3}
# converting class label strings into numerical classlabels
for y_value in YData:
    for key, value in ClassLabelNumerical.items():
        if y_value == key:
            YVectorData.append(value)

YVectorData = pd.DataFrame(YVectorData)

#initializing train test vectors
Xtrain = pd.DataFrame(columns=[0, 1, 2, 3])
Xtest = pd.DataFrame(columns=[0, 1, 2, 3])
ytrain = pd.DataFrame(columns=[0])
ytest = pd.DataFrame(columns=[0])


def Kfold_Iris_LR():
    #applying k-fold on the data
    fold = [3,4,5,10]
    for i in fold:
        foldval = i
        kf = KFold(len(YVectorData), n_folds=foldval, shuffle=True)
        sumacc = 0
        sumerr = 0
        for train_indices, test_indices in kf:
            trainIndexLen = len(train_indices)
            testIndexLen = len(test_indices)
            for i in range(0,trainIndexLen):
                trainIndexVal = train_indices[i]
                XtrainVal = XVectorData.iloc[trainIndexVal]
                Xtrain.loc[i] = list(XtrainVal)
                YtrainVal = YVectorData.iloc[trainIndexVal]
                ytrain.loc[i] = list(YtrainVal)
            for j in range(0,testIndexLen):
                testIndexVal = test_indices[j]
                Xtest.loc[j] = list(XVectorData.iloc[testIndexVal])
                ytest.loc[j] = list(YVectorData.iloc[testIndexVal])
            # finding A'.A
            A_transposeA = np.dot(Xtrain.transpose(), Xtrain).astype(np.float64)
            # finding dot product of (A'.A) inverse and A' vector
            AtA_At = np.dot(np.linalg.pinv(A_transposeA), Xtrain.transpose()).astype(np.float64)
            # finding beta
            B_hat = np.dot(AtA_At, ytrain)
            # find y predictions with B_hat and Xtest
            y_pred = np.dot(Xtest, B_hat)
            y_pred = pd.DataFrame(y_pred)
            y_pred[0] = y_pred[0].apply(lambda x: int(round(x,0)))
            #print(y_pred)
            #finding accuracy, mean squared error with y_pred and y_test
            ytestarr = [x for x in ytest[0]]
            ypredarr = [y for y in y_pred[0]]
            accuracy = accuracy_score(ytestarr, ypredarr, normalize=True)
            #print("accuracy with ", i, "-fold: ", round(accuracy * 100, 2),"%")
            sumacc = sumacc + accuracy
            errorscore = mean_squared_error(ytestarr, ypredarr)
            #print("mean squared error with ", i, "-fold: ", round(errorscore * 100, 2), "%")
            sumerr = sumerr + errorscore
        avg_acc = sumacc / foldval
        avg_err = sumerr / foldval
        print("Average Accuracy for ", foldval,"-fold: ", round(avg_acc*100, 2), "%")
        print("Average Mean Squared Error for ", foldval,"-fold: ", round(avg_err*100, 2), "%")

Kfold_Iris_LR()