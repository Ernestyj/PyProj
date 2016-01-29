# -*- coding: utf-8 -*-
__author__ = 'DCLab'

import urllib2
from BeautifulSoup import *
from urlparse import urljoin
import sqlite3 as sqlite
import ex_nn
import BeautifulSoup as BeautifulSoup

# 忽略单词列表
ignorewords = {'the': 1, 'of': 1, 'to': 1, 'and': 1, 'a': 1, 'in': 1, 'is': 1, 'it': 1}


class crawler:
    def __init__(self, dbname):
        pass

    def __del__(self):
        pass

    def dbcommit(self):
        pass

    # 获取条目id，若不存在则加入数据库
    def getentryid(self, table, field, value, createnew=True):
        return None

    # 为每个网页建立索引
    def addtoindex(self, url, soup):
        print('Indexing %s', url)

    # 从html页面中提取文字（不带标签）
    def gettextonly(self, text):
        return None

    # 根据任何非空白字符进行分词处理
    def separatewords(self, text):
        return None

    # 如果url已经建立过索引，返回true
    def isindexed(self, url):
        return False

    # 添加关联两个页面的链接
    def addlinkref(self, urlFrom, urlTo, linkText):
        pass

    # 从一小组网页开始BFS直到给定深度，同时为网页建立索引
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=urllib2.urlopen(page)
                except:
                    print 'Could not open %s' % page
                    continue

                try:
                    soup = BeautifulSoup(c.read())
                    self.addtoindex(page, soup)
                    links = soup('a')
                    for link in links:
                        if ('href' in dict(link.attrs)):
                            url = urljoin(page, link['href'])
                            if url.find("'") != -1: continue
                            url = url.split('#')[0]  # 去掉位置部分
                            if url[0:4] == 'http' and not self.isindexed(url):
                                newpages[url] = 1
                            linkText = self.gettextonly(link)
                            self.addlinkref(page, url, linkText)
                    self.dbcommit()
                except:
                    print "Could not parse page %s" % page
            pages = newpages

    # 创建数据库表
    def createindextables(self):
        pass

    def calculatepagerank(self, iterations=20):
        pass


