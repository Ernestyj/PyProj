# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy import *
import os
from time import sleep


def loadDataSet(fileName=os.getcwd()+'/data/testSet_svm.txt'):
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

'''
SMO算法中的外循环确定要优化的最佳alpha对。
而简化版却会跳过这一部分，首先在数据集上遍历每一个alpha,
然后在剩下的alpha集合中随机选择另一个alpha ，从而构建alpha对.
里有一点相当重要，就是我们要同时改变两个alpha.
'''

'''在某个区间范围内随机选择一个整数(alpha的下标)
i是第一个alpha的下标
alphaNum是所有alpha的数目
只要函数值不等于输人值i，函数就会进行随机选择
'''
def selectJrand(i, alphaNum):
    j=i #we want to select any J not equal to i
    while (j==i):
        j = int(random.uniform(0, alphaNum))
    return j

'''在数值太大时对随机选出的值进行调整
是用于调整大于H或小于L的alpha值
'''
def clipAlpha(aj,H,L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

'''简化版SMO
创建一个alpha向量并将其初始化为0向量
当迭代次数小于最大迭代次数时（外循环）
    对数据集中的每个数据向量（内循环）：
        如果该数据向量可以被优化：
            随机选择另外一个数据向量
            同时优化这两个向量
            如果两个向量都不能被优化，退出内循环
    如果所有向量都没被优化，增加迭代数目，继续下一次循环
'''
def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose()
    b = 0; m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while (iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b
            Ei = fXi - float(labelMat[i])
            # 如果误差很大,那么可以对该数据实例所对应的alpha值进行优化
            # if checks if an example violates KKT conditions
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):
                # 随机选择第二个alpha
                j = selectJrand(i,m)
                fXj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy(); alphaJold = alphas[j].copy();
                # 计算L和H,用于调整alpha在0和C之间
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                # 如果L和H相等，就不做任何改变
                if L==H: print "L==H"; continue
                # eta是alpha[j]的最优修改量
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                # 如果eta为O,需要退出for循环的当前迭代过程(该过程对真实SMO算法进行了简化处理。如果eta为0那么计算新的alpha[j]就比较麻烦了)
                if eta >= 0: print "eta>=0"; continue
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                # 检查alpha[j]是否有轻微改变。如果是的话，就退出for循环
                if (abs(alphas[j] - alphaJold) < 0.00001): print "j not moving enough"; continue
                # alpha[i]和alpha[j]同样进行改变，虽然改变的大小一样，但是改变的方向正好相反（即如果一个增加，那么另外一个减少）
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])#update i by the same amount as j(the update is in the oppostie direction)
                # 在对alpha[i]和alpha[j]进行优化之后，给这两个alpha值设置一个常数项b
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2)/2.0

                alphaPairsChanged += 1
                print "iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
        # 只有在所有数据集上遍历maxiter次，且不再发生任何alpha修改之后，程序才会停止并退出while循环。
        if (alphaPairsChanged == 0): iter += 1
        else: iter = 0
        print "iteration number: %d" % iter
    return b,alphas

def test_1():
    dataArrList, labelArrList = loadDataSet()
    b, alphas = smoSimple(dataArrList, labelArrList, C=0.6, toler=0.001, maxIter=40)
    print b
    print alphas[alphas>0]
    print '支持向量有:'
    for i in range(len(dataArrList)):
        if alphas[i]>0.0: print dataArrList[i], labelArrList[i]

test_1()