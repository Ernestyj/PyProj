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

def optimizeAdaBoost(X_norm, y, clf, kFolds=10):
    clf = pipeline.Pipeline([
        ('ada', clf),
    ])
    # grid search 多参数优化
    parameters = {
        # 'ada__n_estimators': np.logspace(0, 3, 20),
        'ada__n_estimators': np.linspace(1, 100, 10, dtype=np.dtype(np.int16)),
        # 'svc__gamma': np.linspace(0, 50, 20),
    }
    gs = grid_search.GridSearchCV(clf, parameters, verbose=1, refit=False, cv=kFolds)
    gs.fit(X_norm, y)
    return gs.best_params_['ada__n_estimators'], gs.best_score_

lr_l1 = LogisticRegression(C=100, penalty='l1', tol=0.01)
lr_l2 = LogisticRegression(C=100, penalty='l2', tol=0.01)

rf = RandomForestClassifier(max_depth=5, min_samples_split=2)
et = ExtraTreesClassifier(max_depth=20, min_samples_split=2)

dt_stump = DecisionTreeClassifier(max_depth=1, min_samples_leaf=1)
dt_9_1 = DecisionTreeClassifier(max_depth=9, min_samples_leaf=1)
dt_20_1 = DecisionTreeClassifier(max_depth=20, min_samples_leaf=1)

clf_default = AdaBoostClassifier(n_estimators=100)
clf_stump = AdaBoostClassifier(base_estimator=dt_stump, n_estimators=100)
clf_dt = AdaBoostClassifier(base_estimator=dt_9_1, n_estimators=100)
# clf_dt = AdaBoostClassifier(base_estimator=dt_20_1, n_estimators=100)

clf_svc_linear = AdaBoostClassifier(SVC(probability=True, kernel='linear'))
clf_svc_rbf = AdaBoostClassifier(SVC(probability=True, kernel='rbf'))
clf_svc_poly = AdaBoostClassifier(SVC(probability=True, kernel='poly'))

clf_sgd_hinge = AdaBoostClassifier(SGDClassifier(loss='hinge'), algorithm='SAMME')
clf_sgd_logistic = AdaBoostClassifier(SGDClassifier(loss='log'))
clf_sgd_modified_huber = AdaBoostClassifier(SGDClassifier(loss='modified_huber'))

clf_ridge = AdaBoostClassifier(RidgeClassifier(), algorithm='SAMME')

clf_rf = AdaBoostClassifier(rf)

bag_default = BaggingClassifier(n_estimators=100)
bag_stump = BaggingClassifier(base_estimator=dt_stump, n_estimators=100)
bag_sgd_hinge = BaggingClassifier(SGDClassifier(loss='hinge'))
bag_sgd_logistic = BaggingClassifier(SGDClassifier(loss='log'))


# evaluate_cross_validation(clf_sgd_hinge, X_norm, y, 10)
n_estimators, score = optimizeAdaBoost(X_norm, y, clf=clf_svc_rbf, kFolds=10)
print 'n_estimators=',n_estimators, 'score=',score