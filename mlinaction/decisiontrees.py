# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import operator
from math import log

def test_createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

dataSet, labels = test_createDataSet()

'''Shannon Entropy
'''
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featureVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featureVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    entropy = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        entropy -= prob * log(prob,2) #log base 2
    return entropy


'''划分数据集(按照给定特征)
输入:
dataSet:待划分的数据集
axis:划分数据集的特征
value:特征的返回值
输出:
划分好的数据集
'''
def splitDataSet(dataSet, axis, value):
    resultDataSet = []
    for featureVec in dataSet:
        if featureVec[axis] == value:
            reducedFeatVec = featureVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend(featureVec[axis+1:])
            resultDataSet.append(reducedFeatVec)
    return resultDataSet


'''选择最好的数据集划分方式
'''
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1      #the last column is used for the labels
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):        #iterate over all the features
        featList = [example[i] for example in dataSet]#create a list of all the examples of this feature
        uniqueVals = set(featList)       #get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy     #calculate the info gain; ie reduction in entropy
        if (infoGain > bestInfoGain):       #compare this to the best gain so far
            bestInfoGain = infoGain         #if better than current best, set to best
            bestFeature = i
    return bestFeature                      #returns an integer


'''投票表决
'''
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


'''创建树(递归)
'''
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    #stop splitting when all of the classes are equal
    if classList.count(classList[0]) == len(classList): return classList[0]
    #stop splitting when there are no more features in dataSet
    if len(dataSet[0]) == 1: return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree
