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
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

from sklearn import preprocessing, svm, cross_validation, metrics, pipeline, grid_search
from scipy.stats import sem
from sklearn.decomposition import PCA, KernelPCA

'''
读入一支股票指定年份的ohlcv数据
输入:baseDir,stockCode为字符, startYear,yearNum为整数，
输出:dataframe
'''
def readWSDFile(baseDir, stockCode, startYear, yearNum=1):
    # 解析日期
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d').date()

    df = 0
    for i in range(yearNum):
        tempDF = pd.read_csv(baseDir+stockCode+'/wsd_'+stockCode+'_'+str(startYear+i)+'.csv',
                                index_col=0, sep='\t', usecols=[0,2,3,4,5,6,7,9,10,12,15], header=None,
                                skiprows=1, names=['Date','Open','High','Low','Close','Volume','Amount',
                                                   'Chg','Chg Pct','Avg','Turn'],
                               parse_dates=True, date_parser=dateparse)
        if i==0: df = tempDF
        else: df = df.append(tempDF)
    return df



usecols = [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
           21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 36, 37]
usecols = [0, 6, 16, 17, 24, 31]
def readWSDIndexFile(baseDir, stockCode, startYear, yearNum=1):
    # 解析日期
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d').date()

    df = 0
    for i in range(yearNum):
        tempDF = pd.read_csv(baseDir+'I'+stockCode+'/wsd_'+stockCode+'_'+str(startYear+i)+'.csv',
                                index_col=0, sep=',', parse_dates=True, date_parser=dateparse, usecols=usecols)
        if i==0: df = tempDF
        else: df = df.append(tempDF)
    return df


def prepareData(df, dfi, win=5):
    # open（开盘价均值）,high（最高价均值）,low（最低价均值）,volume（成交量均值）,amount（成交额均值）,
    # change（涨跌均值）,changePct（涨跌幅均值）,average（均价均值）,turn（换手率均值）,
    # r(收益率均值),
    # 38种技术指标
    open = pd.rolling_mean(df['Open'], window=win)
    high = pd.rolling_mean(df['High'], window=win)
    low = pd.rolling_mean(df['Low'], window=win)
    volume = pd.rolling_mean(df['Volume'], window=win)
    amount = pd.rolling_mean(df['Amount'], window=win)
    change = pd.rolling_mean(df['Chg'], window=win)
    changePct = pd.rolling_mean(df['Chg Pct'], window=win)
    average = pd.rolling_mean(df['Avg'], window=win)
    turn = pd.rolling_mean(df['Turn'], window=win)
    dailyreturn = df['Close'].pct_change()
    dailyreturn[0] = dailyreturn[1]
    r = pd.rolling_mean(dailyreturn, window=win)

    techDF = pd.rolling_mean(dfi, window=win)

    tempX = np.column_stack((open[win-1:], high[win-1:], low[win-1:], volume[win-1:], amount[win-1:],
                        change[win-1:], changePct[win-1:], average[win-1:], turn[win-1:], r[win-1:]))

    X = np.hstack((tempX, techDF.values[win-1:]))
    y = []
    for i in range(win-1, len(dailyreturn)):
        if dailyreturn[i]<0: y.append(-1)
        elif dailyreturn[i]>0: y.append(1)
        else: y.append(y[-1])   # 按前一个值填充
    return X, y


def optimizeSVM(X_norm, y, kFolds=10):
    clf = pipeline.Pipeline([
        ('svc', svm.SVC(kernel='rbf')),
    ])
    # grid search 多参数优化
    parameters = {
        # 'svc__gamma': np.logspace(-1, 3, 20),
        # 'svc__C': np.logspace(-1, 3, 10),
        # 'svc__gamma': np.logspace(-3, 11, 8, base=2),
        # 'svc__C': np.logspace(-3, 15, 10, base=2),
        'svc__gamma': np.logspace(-3, 11, 8, base=2),
        'svc__C': np.logspace(-3, 15, 10, base=2),
    }
    gs = grid_search.GridSearchCV(clf, parameters, verbose=1, refit=False, cv=kFolds)
    gs.fit(X_norm, y)
    return gs.best_params_['svc__gamma'], gs.best_params_['svc__C'], gs.best_score_


def plot3D(X_pca, y):
    red_x, red_y, red_z = [], [], []
    blue_x, blue_y, blue_z = [], [], []
    for i in range(len(X_pca)):
        if y[i]==-1:
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

baseDir = '/Users/eugene/Downloads/data/'
stockCodes = ['000300.SH', '000016.SH', '000905.SH']


i = 0
startYear = 2014
number = 2
df = readWSDFile(baseDir, stockCodes[i], startYear, number)
print 'Day count:', len(df)
# print df.head(5)
dfi = readWSDIndexFile(baseDir, stockCodes[i], startYear, number)
X, y = prepareData(df, dfi, win=12)
print np.shape(X), np.shape(y)
# print np.shape(X)
normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
X_norm = normalizer.transform(X)

# estimator = PCA(n_components=10)
# estimator_kernel = KernelPCA(n_components=12, kernel='rbf')
# # X_pca = estimator.fit_transform(X_norm)
# X_pca = estimator_kernel.fit_transform(X_norm)

# plot3D(X_pca, y)

# grid search 多参数优化
gamma, C, score = optimizeSVM(X_norm, y, kFolds=10)
print 'gamma=',gamma, 'C=',C, 'score=',score