#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

import math

# Step1：时间序列分段
# 子区间长度n是可变的，如果进行回归分析需要进行将时间序列进行分段，例如若时间序列长度为240，则其可以分解成4段长度为60的等长子区间，
# 或者6段长度为40的等长子区间……
'''
输入：数据长度
输出：分段方案矩阵
'''
def getSegmentationMatrix(dataLen):
    segmentMatrix = []
    end = math.floor(dataLen/4)
    for i in range(4, int(end+1)):
        if dataLen%i==0:
            segmentMatrix.append([i, dataLen/i])
    return segmentMatrix


# step2：Hurst指数计算
'''
输入：时间序列数组
输出：hurst指数值
'''
# def computeHurst1(data):
#     data = np.array(data).astype('float')
#     dataLen = len(data)
#     segmentMatrix = getSegmentationMatrix(dataLen)
#     segMethod = len(segmentMatrix)#分段方案数
#     logRS = np.zeros(segMethod)
#     logN = np.zeros(segMethod)
#     for i in range(0, segMethod):
#         dataMat = data.reshape(segmentMatrix[i])
#         m = segmentMatrix[i][0]
#         n = segmentMatrix[i][1]
#         meanArr = dataMat.mean(axis=1)
#         # 计算第a个区间的累计离差(转置)
#         subMatTrans = dataMat.T-meanArr
#         cumSubMat = subMatTrans.T.cumsum(axis=1)
#         RVector = np.zeros(n*m).reshape(n, m)
#         SVector = np.zeros(n*m).reshape(n, m)
#         # 计算(R/S)n
#         for j in range(n):
#             RVector[j] = cumSubMat[:,:j+1].max(axis=1)-cumSubMat[:,:j+1].min(axis=1)
#             SVector[j] = dataMat[:,:j+1].std(axis=1)
#         logRS[i] = math.log((RVector/SVector).T.mean(axis=1).mean())
#         logN[i] = math.log(n)
#     return np.polyfit(logN, logRS, 1)[0]
def computeHurst(data):
    data = np.array(data).astype('float')
    dataLen = len(data)
    segmentMatrix = getSegmentationMatrix(dataLen)
    segMethod = len(segmentMatrix)#分段方案数
    logRS = np.zeros(segMethod)
    logN = np.zeros(segMethod)
    for i in range(0, segMethod):
        dataMat = data.reshape(segmentMatrix[i])
        m = segmentMatrix[i][0]
        n = segmentMatrix[i][1]
        meanArr = dataMat.mean(axis=1)
        # 计算第a个区间的累计离差(转置)
        subMatTrans = dataMat.T-meanArr
        cumSubMat = subMatTrans.T.cumsum(axis=1)
        # 计算(R/S)n
        RVector = cumSubMat.max(axis=1)-cumSubMat.min(axis=1)
        SVector = dataMat.std(axis=1)
        logRS[i] = math.log((RVector/SVector).mean())
        logN[i] = math.log(n)
    return np.polyfit(logN, logRS, 1)[0]


# step3：移动平均hurst指数计算
# 例如计算120个交易日的Husrt指数，使用的数据为[t-119,t]的价格数据即可，移动平均的意思为根据t的向前移动，
# 计算指数的数据[t-119,t]的价格数据同时根据t进行移动。
'''
输入：以时间为索引的Series
输出：以时间为索引的hurst Series
'''
def computeMovingHurst(dataSeries, window=120):
    dataLen = len(dataSeries)
    if dataLen<window:
        print 'window length is bigger than data length'
        return
    logPrices = np.log(dataSeries.values)
    indexReturns = np.append([0], np.diff(logPrices))
    hursts = np.zeros(dataLen)
    hursts[0:window] = np.NaN
    for i in range(dataLen-window):
        hursts[window+i] = computeHurst(indexReturns[i:i+window])
    return pd.Series(hursts, index=dataSeries.index)

# 计算E(H),用Peters方法计算E[(R/S)n]
'''
输入：时间序列数组
输出：hurst指数期望值
'''
def computeHurstExpecPeters(data):
    dataLen = len(data)
    segmentMatrix = getSegmentationMatrix(dataLen)
    segMethod = len(segmentMatrix)#分段方案数
    logERS = np.zeros(segMethod)
    logN = np.zeros(segMethod)
    for i in range(0, segMethod):
        n = segmentMatrix[i][1]
        # 用Peters方法计算E[(R/S)n]
        tempSum = 0
        for r in range(1, n):
            tempSum += math.sqrt((n-1)/r)
        ERS = (n-0.5)/n * math.pow(n*math.pi/2, -0.5) * tempSum
        logERS[i] = math.log(ERS)
        logN[i] = math.log(n)
    return np.polyfit(logN, logERS, 1)[0]