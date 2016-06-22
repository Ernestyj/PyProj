#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import talib
import math

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
i = 0
startYear = 2014
yearNum = 2

df = readWSDFile(baseDir, instruments[i], startYear, yearNum)
print 'Day count:', len(df)
# print df.head(5)
dfi = readWSDIndexFile(baseDir, instruments[i], startYear, yearNum)

X, y, actionDates = prepareData(df, dfi, win=16)
print np.shape(X)
normalizer = preprocessing.Normalizer().fit(X)  # fit does nothing
X_norm = normalizer.transform(X)


def optimizeEnsemble(X_norm, y, clf, kFolds=10):
    clf = pipeline.Pipeline([
        ('ensemble', clf),
    ])
    # grid search 多参数优化
    parameters = {
        'ensemble__n_estimators': np.linspace(1, 200, 20, dtype=np.dtype(np.int16)),
    }
    gs = grid_search.GridSearchCV(clf, parameters, verbose=1, refit=False, cv=kFolds)
    gs.fit(X_norm, y)
    return gs.best_params_['ensemble__n_estimators'], gs.best_score_

def evaluate_cross_validation(clf, X, y, K):
    from scipy.stats import sem
    cv = cross_validation.KFold(len(y), K, shuffle=True, random_state=0)
    scores = cross_validation.cross_val_score(clf, X, y, cv=cv)
    print '*********************************evaluate_cross_validation*********************************'
    print "scores:", scores
    print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))


rf = RandomForestClassifier(max_depth=None, min_samples_split=2, max_features='sqrt', n_estimators=200, random_state=47)
et = ExtraTreesClassifier(max_depth=None, min_samples_split=1, max_features=7)


# evaluate_cross_validation(rf, X_norm, y, 10)
# n_estimators, score = optimizeEnsemble(X_norm, y, clf=rf, kFolds=10)
# print 'n_estimators=',n_estimators, 'score=',score
