# -*- coding: utf-8 -*-
from sklearn import datasets

def test_1():
    X, y = datasets.make_classification(n_samples=1000, n_features=3, n_redundant=0)
    # print X
    # print y

    from sklearn.tree import DecisionTreeClassifier
    dt = DecisionTreeClassifier()
    classifier = dt.fit(X, y)
    print classifier

    preds = dt.predict(X)
    # print preds
    print (preds==y).mean()

test_1()


