#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 30)
pd.set_option('precision', 7)
pd.options.display.float_format = '{:,.3f}'.format

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
                                index_col=0, sep='\t', usecols=[0,2,3,4,5,6,7], header=None,
                                skiprows=1, names=['Date','OPEN','HIGH','LOW','CLOSE','VOLUME','AMOUNT'],
                               parse_dates=True, date_parser=dateparse)
        if i==0: df = tempDF
        else: df = df.append(tempDF)
    return df


def prepareData(df):
    # high（周最高价均值）, low（周最低价均值）, r(周收益率), lastR(上周收益率), weekAgoR（前周收益率）,
    # amt（周成交额均值）, lastAmt(上周成交额均值),fourWeekAvgAmt（近四周成交额均值）
    #跳过第一个值
    highs = [0]; highArr = []
    lows = [0]; lowArr = []
    rs = [0]; closeArr = []
    lastRs = [0];
    weekAgoRs = [0];
    amts = [0]; amtArr = []
    lastAmts = [0];
    upOrDowns = [0] #为0表示跌，为1表示涨
    actionDates = [0]
    # fourWeekAvgAmts = [0];#暂不加入计算
    week = df.index[0].week
    for i in range(len(df)):
        if week!=df.index[i].week:
            highs.append(np.mean(highArr))
            lows.append(np.mean(lowArr))
            rs.append((closeArr[-1]-closeArr[0])/closeArr[0])
            lastRs.append(rs[-2])
            weekAgoRs.append(lastRs[-2])
            amts.append(np.mean(amtArr))
            lastAmts.append(amts[-2])
            upOrDown = 0
            if rs[-1]>0.0: upOrDown = 1
            elif rs[-1]==0.0: upOrDown = upOrDowns[-1] # 无涨跌时，按前周的涨跌情况
            else: upOrDown = 0
            upOrDowns.append(upOrDown)
            actionDates.append(df.index[i].date())
            del highArr[:]
            del lowArr[:]
            del closeArr[:]
            del amtArr[:]
            week = df.index[i].week
        highArr.append(df['HIGH'][i])
        lowArr.append(df['LOW'][i])
        closeArr.append(df['CLOSE'][i])
        amtArr.append(df['AMOUNT'][i])
    #处理最后一周数据
    highs.append(np.mean(highArr))
    lows.append(np.mean(lowArr))
    rs.append((closeArr[-1]-closeArr[0])/closeArr[0])
    lastRs.append(rs[-2])
    weekAgoRs.append(lastRs[-2])
    amts.append(np.mean(amtArr))
    lastAmts.append(amts[-2])
    upOrDown = 0
    if rs[-1]>0.0: upOrDown = 1
    elif rs[-1]==0.0: upOrDown = upOrDowns[-1] # 无涨跌时，按前周的涨跌情况
    else: upOrDown = 0
    upOrDowns.append(upOrDown)
    actionDates.append(df.index[i].date())

    X = np.column_stack((highs[1:], lows[1:], rs[1:], lastRs[1:], weekAgoRs[1:], amts[1:], lastAmts[1:]))
    y = upOrDowns[2:]   # 涨跌数组向后移一位,表当前周数据预测下一周涨跌
    y.append(upOrDowns[-1]) # 涨跌数组最后一位按前一位数据补上
    return X, y, actionDates[1:]


def evaluate_cross_validation(clf, X, y, K):
    cv = cross_validation.KFold(len(y), K, shuffle=True, random_state=0)
    scores = cross_validation.cross_val_score(clf, X, y, cv=cv)
    print '*********************************evaluate_cross_validation*********************************'
    print "scores:", scores
    print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))

def train_and_evaluate(clf, X_train, X_test, y_train, y_test):
    clf.fit(X_train, y_train)
    print "Accuracy on training set:", clf.score(X_train, y_train)
    print "Accuracy on testing set:", clf.score(X_test, y_test)
    y_pred = clf.predict(X_test)
    print "Classification Report:\n", metrics.classification_report(y_test, y_pred)
    print "Confusion Matrix:\n", metrics.confusion_matrix(y_test, y_pred)

def calc_params(X, y, clf, param_values, param_name, K):
    # initialize training and testing scores with zeros
    train_scores = np.zeros(len(param_values))
    test_scores = np.zeros(len(param_values))
    # iterate over the different parameter values
    for i, param_value in enumerate(param_values):
        print param_name, ' = ', param_value
        # set classifier parameters
        clf.set_params(**{param_name:param_value})
        # initialize the K scores obtained for each fold
        k_train_scores = np.zeros(K)
        k_test_scores = np.zeros(K)
        # create KFold cross validation
        cv = cross_validation.KFold(len(y), K, shuffle=True, random_state=0)
        # iterate over the K folds
        for j, (train, test) in enumerate(cv):
            # fit the classifier in the corresponding fold and obtain the corresponding accuracy scores on train and test sets
            clf.fit([X[k] for k in train], [y[k] for k in train])
            k_train_scores[j] = clf.score([X[k] for k in train], [y[k] for k in train])
            k_test_scores[j] = clf.score([X[k] for k in test], [y[k] for k in test])
        # store the mean of the K fold scores
        train_scores[i] = np.mean(k_train_scores)
        test_scores[i] = np.mean(k_test_scores)
    # plot the training and testing scores in a log scale
#     plt.semilogx(param_values, train_scores, alpha=0.4, lw=2, c='b')
#     plt.semilogx(param_values, test_scores, alpha=0.4, lw=2, c='g')
    plt.plot(param_values, train_scores, alpha=0.4, lw=2, c='b')
    plt.plot(param_values, test_scores, alpha=0.4, lw=2, c='g')
    plt.xlabel(param_name + " values")
    plt.ylabel("Mean cross validation accuracy")
    # return the training and testing scores on each parameter value
    return train_scores, test_scores

def optimizeSVM(X_norm, y, kFolds=10):
    clf = pipeline.Pipeline([
        ('svc', svm.SVC(kernel='rbf')),
    ])
    # grid search 多参数优化
    parameters = {
        'svc__gamma': np.logspace(0, 3, 20),
        'svc__C': np.logspace(0, 3, 10),
        # 'svc__gamma': np.linspace(0, 50, 20),
        # 'svc__C': np.linspace(0.001, 30, 10),
    }
    gs = grid_search.GridSearchCV(clf, parameters, verbose=1, refit=False, cv=kFolds)
    gs.fit(X_norm, y)
    return gs.best_params_['svc__gamma'], gs.best_params_['svc__C'], gs.best_score_


# baseDir = '/Users/eugene/Downloads/data/'
# stockCodes = ['000300.SH', '000016.SH', '000905.SH']
#
# df = readWSDFile(baseDir, stockCodes[0], 2014, 2)
# print 'Day count:', len(df)
# X, y, actionDates = prepareData(df)
# normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
# # normalizer = preprocessing.StandardScaler().fit(X)
# X_norm = normalizer.transform(X)
#
# estimator = PCA(n_components=7)
# estimator_kernel = KernelPCA(n_components=7, kernel='rbf')
# X_pca = estimator.fit_transform(X_norm)
# # X_pca = estimator_kernel.fit_transform(X_norm)
#
# # grid search 多参数优化
# gamma, C, score = optimizeSVM(X_norm, y, kFolds=10)
# print 'gamma=',gamma, 'C=',C, 'score=',score

# # model selection 单参数优化
# clf = pipeline.Pipeline([
#     ('svc', svm.SVC(kernel='rbf')),
# ])
# gammas = np.logspace(-2, 1, 10)
# gammas = np.linspace(0,5,10)
# train_scores, test_scores = calc_params(X_norm, y, clf, gammas, 'svc__gamma', 3)
# print 'training scores: ', train_scores
# print 'testing scores: ', test_scores

# X_train, X_test, y_train, y_test = cross_validation.train_test_split(X_norm, y, test_size=0.25, random_state=0)
# rbf_svc = svm.SVC(kernel='rbf', gamma=gamma, C=C)
# train_and_evaluate(rbf_svc, X_train, X_test, y_train, y_test)