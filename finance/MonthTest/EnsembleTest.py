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

from MonthDataPrepare import readWSDFile, prepareData, optimizeSVM, readWSDIndexFile, readAndCombineMacroEconomyFile, readMoneySupplyFile


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

df = readWSDFile(baseDir, instrument, startYear=startYear, yearNum=yearNum)
print 'Day count:', len(df)
dfi = readWSDIndexFile(baseDir, instrument, startYear, yearNum)
dfmacro = readAndCombineMacroEconomyFile(baseDir, startYear, yearNum=yearNum)
dfmoney = readMoneySupplyFile(baseDir, 'money_supply.csv', startYear, yearNum=yearNum)
X, y, actionDates = prepareData(df, dfi, dfmacro, dfmoney)
print np.shape(X), np.shape(y)

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

# evaluate_cross_validation(rf, X_norm, y, 10)
# n_estimators, score = optimizeEnsemble(X_norm, y, clf=rf, kFolds=10)
# print 'n_estimators=',n_estimators, 'score=',score
