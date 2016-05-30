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

from SVMTest import readWSDFile, prepareData, optimizeSVM, evaluate_cross_validation, train_and_evaluate

from sklearn import preprocessing, cross_validation, metrics, pipeline, grid_search
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier, LogisticRegression, RidgeClassifier
from sklearn.tree import DecisionTreeClassifier

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


def optimizeAdaBoostSGD(X_norm, y, kFolds=10):
    # grid search 多参数优化
    parameters = {
        'base_estimator__alpha': 10.0 ** (-np.arange(1, 7)),
        'n_estimators': np.linspace(1, 100, 10, dtype=np.dtype(np.int16)),
    }
    # sgd = SGDClassifier(loss='log', n_iter=np.ceil(10**6/len(X_norm)))
    sgd = SGDClassifier(loss='log', n_iter=5)
    clf = AdaBoostClassifier(base_estimator=sgd)

    gs = grid_search.GridSearchCV(clf, parameters, verbose=1, refit=False, cv=kFolds)
    gs.fit(X_norm, y)
    return gs.best_params_['base_estimator__alpha'], gs.best_params_['n_estimators'], gs.best_score_

alpha, n_estimators, score = optimizeAdaBoostSGD(X_norm, y, kFolds=10)
print 'alpha',alpha, 'n_estimators=',n_estimators, 'score=',score