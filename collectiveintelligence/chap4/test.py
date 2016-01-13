# -*- coding: utf-8 -*-
__author__ = 'DCLab'

import searchengine

pagelist=['http://www.baidu.com']
crawler=searchengine.crawler('')
crawler.crawl(pagelist)
print('****************************************************************************************')
