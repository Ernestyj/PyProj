# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import operator
import os


'''kNN: k Nearest Neighbors
Input:
inX: vector to compare to existing dataset (1xN)
dataSet: size m data set of known vectors (NxM)
labels: data set labels (1xM vector)
k: number of neighbors to use for comparison (should be an odd number)
Output:
the most popular class label
'''
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def test_1():
    df = pd.read_csv(os.getcwd()+'/data/datingTestSet.txt', sep='\t', header=None)
    datingDataMat = df.as_matrix(columns=[0,1,2])
    datingLabels = df[3].tolist()
    datingLabelsInt = df[3].apply(lambda x: 1 if x=='didntLike' else (2 if x=='smallDoses' else 3))
    fig = plt.figure()
    axe = fig.add_subplot(1,1,1)
    axe.scatter(datingDataMat[:, 0], datingDataMat[:, 1], s=15.0*datingLabelsInt, c=15.0*datingLabelsInt)
    plt.show()

test_1()


'''规一化特征值
newValue = (oldValue-min)/(max-min)
'''
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = np.zeros(np.shape(dataSet))
    rowNum = dataSet.shape[0]
    normDataSet = dataSet - np.tile(minVals, (rowNum, 1))
    normDataSet = normDataSet / np.tile(ranges, (rowNum, 1))
    return normDataSet, ranges, minVals


def datingClassTest():
    holdOutRatio = 0.1 # 用于测试分类器的比例10%，用于训练的比例90%
    # 读入数据
    df = pd.read_csv(os.getcwd()+'/data/datingTestSet.txt', sep='\t', header=None)
    datingDataMat = df.as_matrix(columns=[0,1,2])
    datingLabels = df[3].tolist()
    datingLabelsInt = df[3].apply(lambda x: 1 if x=='didntLike' else (2 if x=='smallDoses' else 3))
    # 规一化
    normMat, ranges, minVals = autoNorm(datingDataMat)

    rowNum = normMat.shape[0]
    numTestVecs = int(rowNum*holdOutRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:rowNum, :], datingLabels[numTestVecs:rowNum], 3)
        # print "the classifier came back with: %s, the real answer is: %s" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the test count is: %d, the error count is: %d" % (numTestVecs, errorCount)
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))

datingClassTest()