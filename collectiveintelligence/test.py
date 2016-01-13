# -*- coding: utf-8 -*-
__author__ = 'DCLab'

import urllib2

c=urllib2.urlopen('https://en.wikipedia.org/wiki/Programming_language')
contents=c.read()
print contents[0:50]