#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import talib

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 30)
pd.set_option('precision', 7)
pd.options.display.float_format = '{:,.3f}'.format

from sklearn import preprocessing
from sklearn.decomposition import PCA, KernelPCA

from SVMTest import readWSDFile, prepareData, optimizeSVM

baseDir = '/Users/eugene/Downloads/Data/'
# baseDir = '/Users/eugene/Downloads/marketQuotationData/'
# 沪深300 上证50 中证500
instruments = ['000300.SH', '000016.SH', '000905.SH']
instrument = instruments[0]
initCapital = 100000000.0 # 一亿
# startYear = 2015; yearNum = 1
startYear = 2014; yearNum = 2

ohlcva = readWSDFile(baseDir, instrument, startYear=startYear, yearNum=yearNum)
print 'Day count:', len(ohlcva)
X, y, actionDates = prepareData(ohlcva)
normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
X_norm = normalizer.transform(X)
# X_norm = X

estimator = PCA(n_components=3)
estimator_kernel = KernelPCA(n_components=3, kernel='rbf')
# X_pca = estimator.fit_transform(X_norm)
X_pca = estimator_kernel.fit_transform(X_norm)


def plot2D(X_pca):
    red_x, red_y = [], []
    blue_x, blue_y = [], []
    for i in range(len(X_pca)):
        if y[i] == 0:
            red_x.append(X_pca[i][0])
            red_y.append(X_pca[i][1])
        elif y[i] == 1:
            blue_x.append(X_pca[i][0])
            blue_y.append(X_pca[i][1])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(red_x, red_y, c='r', marker='x')
    ax.scatter(blue_x, blue_y, c='g', marker='.')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    plt.show()


def plot3D(X_pca):
    red_x, red_y, red_z = [], [], []
    blue_x, blue_y, blue_z = [], [], []
    for i in range(len(X_pca)):
        if y[i]==0:
            red_x.append(X_pca[i][0])
            red_y.append(X_pca[i][1])
            red_z.append(X_pca[i][2])
        elif y[i]==1:
            blue_x.append(X_pca[i][0])
            blue_y.append(X_pca[i][1])
            blue_z.append(X_pca[i][2])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(red_x, red_y, red_z, c='r', marker='x')
    ax.scatter(blue_x, blue_y, blue_z, c='g', marker='.')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


# plot2D(X_pca)
plot3D(X_pca)