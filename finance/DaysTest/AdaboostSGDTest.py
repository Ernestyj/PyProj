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

from DaysDataPrepare import readWSDFile, readWSDIndexFile, prepareData, optimizeSVM

from sklearn import preprocessing, cross_validation, metrics, pipeline, grid_search
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier, LogisticRegression, RidgeClassifier
from sklearn.tree import DecisionTreeClassifier

baseDir = '/Users/eugene/Downloads/Data/'
instruments = ['000300.SH', '000016.SH', '000905.SH']
i = 2
startYear = 2015
yearNum = 1

df = readWSDFile(baseDir, instruments[i], startYear, yearNum)
print 'Day count:', len(df)
# print df.head(5)
dfi = readWSDIndexFile(baseDir, instruments[i], startYear, yearNum)

X, y, actionDates = prepareData(df, dfi, win=16)
print np.shape(X)
normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
X_norm = normalizer.transform(X)


def optimizeAdaBoostSGD(X_norm, y, kFolds=10):
    # grid search 多参数优化
    parameters = {
        # 'base_estimator__alpha': 10.0 ** (-np.arange(1, 7)),
        'base_estimator__alpha': np.logspace(-8, -1, 8),
        # 'n_estimators': np.linspace(1, 100, 10, dtype=np.dtype(np.int16)),
    }
    # sgd = SGDClassifier(loss='log', n_iter=np.ceil(10**6/len(X_norm)))
    sgd = SGDClassifier(loss='log', n_iter=5, random_state=47)
    clf = AdaBoostClassifier(base_estimator=sgd, n_estimators=200, random_state=47)

    gs = grid_search.GridSearchCV(clf, parameters, verbose=1, refit=False, cv=kFolds)
    gs.fit(X_norm, y)
    return gs.best_params_['base_estimator__alpha'], gs.best_score_

def evaluate_cross_validation(clf, X, y, K):
    from scipy.stats import sem
    cv = cross_validation.KFold(len(y), K, shuffle=True, random_state=0)
    scores = cross_validation.cross_val_score(clf, X, y, cv=cv)
    print '*********************************evaluate_cross_validation*********************************'
    print "scores:", scores
    print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))


clf = AdaBoostClassifier(base_estimator=SGDClassifier(loss='log', random_state=47), n_estimators=200, random_state=47)

# evaluate_cross_validation(clf, X_norm, y, 10)
# alpha, score = optimizeAdaBoostSGD(X_norm, y, kFolds=10)
# print 'alpha',alpha, 'score=',score
