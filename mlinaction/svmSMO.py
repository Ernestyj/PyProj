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

'''简化版SMO*********************************************************************************
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

# test_1()
'''**********************************************************************************'''

'''Platt SMO数据结构
'''
class optStruct:
    def __init__(self,dataMatIn, classLabels, C, toler, kTup):  # Initialize the structure with the parameters
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((self.m,1)))
        self.b = 0
        # eCache的第一列给出的是eCache是否有效的标志位，而第二列给出的是实际的E值。
        self.eCache = mat(zeros((self.m,2))) #first column is valid flag
        self.K = mat(zeros((self.m,self.m)))
        for i in range(self.m):
            self.K[:,i] = kernelTrans(self.X, self.X[i,:], kTup)

'''计算E值
'''
def calcEk(optStruc, k):
    fXk = float(multiply(optStruc.alphas, optStruc.labelMat).T * optStruc.K[:, k] + optStruc.b)
    Ek = fXk - float(optStruc.labelMat[k])
    return Ek

'''于选择第二个alpha(内循环的alpha值)(启发式)
目标是选择合适的第二个alpha值以保证在每次优化中采用最大步长
'''
def selectJ(i, optStruc, Ei):         #this is the second choice -heurstic, and calcs Ej
    maxK = -1; maxDeltaE = 0; Ej = 0
    optStruc.eCache[i] = [1, Ei]  #set valid #choose the alpha that gives the maximum delta E
    validEcacheList = nonzero(optStruc.eCache[:, 0].A)[0]
    if (len(validEcacheList)) > 1:
        for k in validEcacheList:   #loop through valid Ecache values and find the one that maximizes delta E
            if k == i: continue #don't calc for i, waste of time
            Ek = calcEk(optStruc, k)
            deltaE = abs(Ei - Ek)
            if (deltaE > maxDeltaE):
                maxK = k; maxDeltaE = deltaE; Ej = Ek
        return maxK, Ej
    else:   #in this case (first time around) we don't have any valid eCache values
        j = selectJrand(i, optStruc.m)
        Ej = calcEk(optStruc, j)
    return j, Ej

'''计算误差值并存人缓存
'''
def updateEk(optStruc, k):#after any alpha has changed update the new value in the cache
    Ek = calcEk(optStruc, k)
    optStruc.eCache[k] = [1, Ek]

'''完整Platt SMO算法的优化例程(内层),类似smoSimple
'''
def innerL(i, oS):
    Ei = calcEk(oS, i)
    if ((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i]*Ei > oS.tol) and (oS.alphas[i] > 0)):
        j,Ej = selectJ(i, oS, Ei) #this has been changed from selectJrand
        alphaIold = oS.alphas[i].copy(); alphaJold = oS.alphas[j].copy();
        if (oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = min(oS.C, oS.alphas[j] + oS.alphas[i])
        if L==H: print "L==H"; return 0
        eta = 2.0 * oS.K[i, j] - oS.K[i, i] - oS.K[j, j] #changed for kernel
        if eta >= 0: print "eta>=0"; return 0
        oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej) / eta
        oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
        updateEk(oS, j) #added this for the Ecache
        if (abs(oS.alphas[j] - alphaJold) < 0.00001): print "j not moving enough"; return 0
        oS.alphas[i] += oS.labelMat[j] * oS.labelMat[i] * (alphaJold - oS.alphas[j])#update i by the same amount as j
        updateEk(oS, i) #added this for the Ecache                    #the update is in the oppostie direction
        b1 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.K[i, i] - oS.labelMat[j] * (oS.alphas[j] - alphaJold) * oS.K[i, j]
        b2 = oS.b - Ej - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.K[i, j] - oS.labelMat[j] * (oS.alphas[j] - alphaJold) * oS.K[j, j]
        if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]): oS.b = b1
        elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]): oS.b = b2
        else: oS.b = (b1 + b2) / 2.0
        return 1
    else: return 0

'''完整Platt SMO算法的外循环
输入和函数smoSimple完全一样
'''
def smoP(dataMatIn, classLabels, C, toler, maxIter,kTup=('lin', 0)):    #full Platt SMO
    oS = optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler, kTup)
    iter = 0
    entireSet = True; alphaPairsChanged = 0
    while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        alphaPairsChanged = 0
        if entireSet:   #go over all
            for i in range(oS.m):
                alphaPairsChanged += innerL(i,oS)
                print "fullSet, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
            iter += 1
        else:#go over non-bound (railed) alphas
            nonBoundIs = nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i,oS)
                print "non-bound, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
            iter += 1
        if entireSet: entireSet = False #toggle entire set loop
        elif (alphaPairsChanged == 0): entireSet = True
        print "iteration number: %d" % iter
    return oS.b,oS.alphas

'''计算w向量
'''
def calcWs(alphas,dataArr,classLabels):
    X = mat(dataArr); labelMat = mat(classLabels).transpose()
    m,n = shape(X)
    w = zeros((n,1))
    for i in range(m):
        w += multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w


'''径向基核函数
'''
def kernelTrans(X, A, kTup): #calc the kernel or transform data to a higher dimensional space
    m,n = shape(X)
    K = mat(zeros((m,1)))
    if kTup[0]=='lin': K = X * A.T   #linear kernel
    elif kTup[0]=='rbf':
        for j in range(m):
            deltaRow = X[j,:] - A
            K[j] = deltaRow*deltaRow.T
        K = exp(K/(-1*kTup[1]**2)) #divide in NumPy is element-wise not matrix like Matlab
    else: raise NameError('Houston We Have a Problem -- That Kernel is not recognized')
    return K

def test_2():
    dataArrList, labelArrList = loadDataSet()
    b, alphas = smoP(dataArrList, labelArrList, C=0.6, toler=0.001, maxIter=40)
    print b
    print alphas[alphas>0]
    print '支持向量有:'
    for i in range(len(dataArrList)):
        if alphas[i]>0.0: print dataArrList[i], labelArrList[i]
    ws = calcWs(alphas, dataArrList, labelArrList)
    print 'w向量:'
    print ws
    dataMat = mat(dataArrList)
    # 如果f大于0 ，那么其属于1类；如果f小于0 ，那么则属于-1类
    f = dataMat[0]*mat(ws)+b
    print '如果f大于0 ，那么其属于1类；如果f小于0 ，那么则属于-1类:\n f=', f

test_2()


'''如果降低σ(K1)，那么训练错误率就会降低，但是测试错误率却会上升。

支持向量的数目存在一个最优值。SVM的优点在于它能对数据进行高效分类。
如果支持向量太少，就可能会得到一个很差的决策边界（下个例子会说明这一点）；
如果支持向量太多，也就相当于每次都利用整个数据集进行分类，这种分类方法称为k近邻。
'''
def test_Rbf(k1=1.3):
    dataArrList,labelArrList = loadDataSet(os.getcwd()+'/data/testSetRBF.txt')
    b,alphas = smoP(dataArrList, labelArrList, 200, 0.0001, 10000, ('rbf', k1)) #C=200 important
    datMat=mat(dataArrList); labelMat = mat(labelArrList).transpose()
    svInd=nonzero(alphas.A>0)[0]
    sVs=datMat[svInd] #get matrix of only support vectors
    labelSV = labelMat[svInd];
    print "there are %d Support Vectors" % shape(sVs)[0]
    m,n = shape(datMat)
    errorCount = 0
    for i in range(m):
        kernelEval = kernelTrans(sVs,datMat[i,:],('rbf', k1))
        predict=kernelEval.T * multiply(labelSV,alphas[svInd]) + b
        if sign(predict)!=sign(labelArrList[i]): errorCount += 1
    print "the training error rate is: %f" % (float(errorCount)/m)
    dataArrList,labelArrList = loadDataSet(os.getcwd()+'/data/testSetRBF2.txt')
    errorCount = 0
    datMat=mat(dataArrList); labelMat = mat(labelArrList).transpose()
    m,n = shape(datMat)
    for i in range(m):
        kernelEval = kernelTrans(sVs,datMat[i,:],('rbf', k1))
        predict=kernelEval.T * multiply(labelSV,alphas[svInd]) + b
        if sign(predict)!=sign(labelArrList[i]): errorCount += 1
    print "the test error rate is: %f" % (float(errorCount)/m)

# test_Rbf()