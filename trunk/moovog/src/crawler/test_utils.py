#! /usr/bin/python2.6
# -*-coding:Utf-8 -* 
from src.crawler.utils import *
print 'creating a new crawler'
myC=crawler() 
print u'myC start_time %s' % (myC.start_time)

#starting the crawl job:

myC.crawl()
myC.saveToDB()

