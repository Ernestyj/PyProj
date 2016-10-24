#!/usr/bin/env python
# -*- coding: utf-8 -*-

def printMsg():
    print 'Hello'

# printMsg()

import nolds
import numpy as np

rwalk = np.cumsum(np.random.random(1000))
h = nolds.hurst_rs(rwalk)
print h