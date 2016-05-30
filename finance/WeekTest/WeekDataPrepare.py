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


# usecols = [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
#            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 36, 37]
usecols = [0,6,16,17,24,31]
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

def prepareData(df, dfi):
    # open（开盘价均值）,high（最高价均值）,low（最低价均值）,volume（成交量均值）,amount（成交额均值）,
    # change（涨跌均值）,changePct（涨跌幅均值）,average（均价均值）,turn（换手率均值）,
    # r(收益率均值),
    # lastR(上周收益率), weekAgoR（前周收益率）, lastAmt(上周成交额均值)
    # 38种技术指标
    # 跳过第一个值
    opens = [0]; openArr = []
    highs = [0]; highArr = []
    lows = [0]; lowArr = []
    volumes = [0]; volumeArr = []
    changes = [0]; changeArr = []
    changePcts = [0]; changePctArr = []
    averages = [0]; averageArr = []
    turns = [0]; turnArr = []
    rs = [0]; closeArr = []
    lastRs = [0]
    weekAgoRs = [0]
    amts = [0]; amtArr = []
    lastAmts = [0]

    techs = []
    techArr = []

    upOrDowns = [0]  # 为0表示跌，为1表示涨
    actionDates = [0]
    # fourWeekAvgAmts = [0];#暂不加入计算
    week = df.index[0].week
    for i in range(len(df)):
        if week != df.index[i].week:
            opens.append(np.mean(openArr))
            highs.append(np.mean(highArr))
            lows.append(np.mean(lowArr))
            volumes.append(np.mean(volumeArr))
            changes.append(np.mean(changeArr))
            changePcts.append(np.mean(changePctArr))
            averages.append(np.mean(averageArr))
            turns.append(np.mean(turnArr))
            rs.append((closeArr[-1] - closeArr[0]) / closeArr[0])
            lastRs.append(rs[-2])
            weekAgoRs.append(lastRs[-2])
            amts.append(np.mean(amtArr))
            lastAmts.append(amts[-2])
            techs.append(np.mean(techArr, axis=0))
            upOrDown = -1
            if rs[-1] > 0.0: upOrDown = 1
            elif rs[-1] == 0.0: upOrDown = upOrDowns[-1]  # 无涨跌时，按前周的涨跌情况
            else: upOrDown = -1
            upOrDowns.append(upOrDown)
            actionDates.append(df.index[i].date())
            del openArr[:]; del highArr[:]; del lowArr[:]; del volumeArr[:]; del changeArr[:]; del changePctArr[:];
            del averageArr[:]; del turnArr[:]; del closeArr[:]; del amtArr[:]
            del techArr[:]
            week = df.index[i].week
        openArr.append(df['Open'][i])
        highArr.append(df['High'][i])
        lowArr.append(df['Low'][i])
        volumeArr.append(df['Volume'][i])
        changeArr.append(df['Chg'][i])
        changePctArr.append(df['Chg Pct'][i])
        averageArr.append(df['Avg'][i])
        turnArr.append(df['Turn'][i])
        closeArr.append(df['Close'][i])
        amtArr.append(df['Amount'][i])
        techArr.append(dfi.iloc[i].values)
    # 处理最后一周数据
    opens.append(np.mean(openArr))
    highs.append(np.mean(highArr))
    lows.append(np.mean(lowArr))
    volumes.append(np.mean(volumeArr))
    changes.append(np.mean(changeArr))
    changePcts.append(np.mean(changePctArr))
    averages.append(np.mean(averageArr))
    turns.append(np.mean(turnArr))
    rs.append((closeArr[-1] - closeArr[0]) / closeArr[0])
    lastRs.append(rs[-2])
    weekAgoRs.append(lastRs[-2])
    amts.append(np.mean(amtArr))
    lastAmts.append(amts[-2])
    techs.append(np.mean(techArr, axis=0))
    upOrDown = -1
    if rs[-1] > 0.0: upOrDown = 1
    elif rs[-1] == 0.0: upOrDown = upOrDowns[-1]  # 无涨跌时，按前周的涨跌情况
    else: upOrDown = -1
    upOrDowns.append(upOrDown)
    actionDates.append(df.index[i].date())

    tempX = np.column_stack((opens[1:], highs[1:], lows[1:], volumes[1:], changes[1:], changePcts[1:], averages[1:],
                         turns[1:], rs[1:], lastRs[1:], weekAgoRs[1:], amts[1:], lastAmts[1:]))
    X = np.hstack((tempX, techs))
    y = upOrDowns[2:]  # 涨跌数组向后移一位,表当前周数据预测下一周涨跌
    y.append(upOrDowns[-1])  # 涨跌数组最后一位按前一位数据补上
    return X, y, actionDates[1:]


def optimizeSVM(X_norm, y, kFolds=10):
    clf = pipeline.Pipeline([
        ('svc', svm.SVC(kernel='rbf')),
    ])
    # grid search 多参数优化
    parameters = {
        'svc__gamma': np.logspace(0, 3, 20),
        'svc__C': np.logspace(0, 3, 10),
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

# baseDir = '/Users/eugene/Downloads/data/'
# stockCodes = ['000300.SH', '000016.SH', '000905.SH']
#
# i = 0
# startYear = 2014
# number = 2
# df = readWSDFile(baseDir, stockCodes[i], startYear, number)
# print 'Day count:', len(df)
# # print df.head(5)
# dfi = readWSDIndexFile(baseDir, stockCodes[i], startYear, number)
#
# X, y, actionDates = prepareData(df, dfi)
# print np.shape(X)
# normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
# X_norm = normalizer.transform(X)
#
# # estimator = PCA(n_components=20)
# # X_pca = estimator.fit_transform(X_norm)
# # estimator_kernel = KernelPCA(n_components=50, kernel='rbf')
# # X_pca = estimator_kernel.fit_transform(X_norm)
# # plot3D(X_pca, y)
#
# # grid search 多参数优化
# gamma, C, score = optimizeSVM(X_norm, y, kFolds=10)
# print 'gamma=',gamma, 'C=',C, 'score=',score