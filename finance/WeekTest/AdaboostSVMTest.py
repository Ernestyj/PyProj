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

from WeekDataPrepare import readWSDFile, readWSDIndexFile, prepareData, optimizeSVM

from sklearn import preprocessing, cross_validation, metrics, pipeline, grid_search
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier, LogisticRegression, RidgeClassifier
from sklearn.tree import DecisionTreeClassifier

baseDir = '/Users/eugene/Downloads/Data/'
instruments = ['000300.SH', '000016.SH', '000905.SH']
i = 0
startYear = 2014
yearNum = 2

df = readWSDFile(baseDir, instruments[i], startYear, yearNum)
print 'Day count:', len(df)
# print df.head(5)
dfi = readWSDIndexFile(baseDir, instruments[i], startYear, yearNum)

X, y, actionDates = prepareData(df, dfi)
print np.shape(X)
normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
X_norm = normalizer.transform(X)


def optimizeAdaBoostSVM(X_norm, y, kFolds=10):
    # grid search 多参数优化
    parameters = {
        'base_estimator__gamma': np.logspace(0, 3, 3),
        'base_estimator__C': np.logspace(0, 3, 3),
        'n_estimators': np.linspace(1, 100, 3, dtype=np.dtype(np.int16)),
    }
    svm = SVC(probability=True, kernel='rbf')
    clf = AdaBoostClassifier(base_estimator=svm)

    gs = grid_search.GridSearchCV(clf, parameters, verbose=1, refit=False, cv=kFolds)
    gs.fit(X_norm, y)
    return gs.best_params_['base_estimator__gamma'], gs.best_params_['base_estimator__C'], gs.best_params_['n_estimators'], gs.best_score_


alpha, C, n_estimators, score = optimizeAdaBoostSVM(X_norm, y, kFolds=10)
print 'alpha',alpha, 'C',C, 'n_estimators=',n_estimators, 'score=',score
