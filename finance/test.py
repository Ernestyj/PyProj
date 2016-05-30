#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import inspect
# from sklearn.utils.testing import all_estimators
# for name, clf in all_estimators(type_filter='classifier'):
#     if 'sample_weight' in inspect.getargspec(clf().fit)[0]:
#        print name


from sklearn.utils.testing import all_estimators
for clf in all_estimators(type_filter='classifier'):
    print clf