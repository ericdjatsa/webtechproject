#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
from sgmllib import SGMLParser
import xml.dom.minidom

headers = {u'User-Agent': u'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/6.0'}

class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []

	def start_a(self, attrs):
		href = [v for k, v in attrs if k == 'href' ]
		if href:
			self.urls.extend(href)

def getTrailerAddictTag(filmName):
	cleanedFilmName = re.sub(u"[:/!#\\$%&\\(\\)\\-\\+\\.\\?\\/'\"]", "", filmName)
	cleanedFilmName = re.sub(u"[öóòóøôõÖÒÓÔÕÖØ]", "o", cleanedFilmName)
	cleanedFilmName = re.sub(u"[àáâåãäÀÁÂÅÃÄ]", "a", cleanedFilmName)
	cleanedFilmName = re.sub(u"[èéêẽëÈÉÊẼË]", "e", cleanedFilmName)
	cleanedFilmName = re.sub(u"[ìíîĩïÌÍÎĨÏ]", "i", cleanedFilmName)
	cleanedFilmName = re.sub(u"[ùúûũüÙÚÛÜŨ]", "u", cleanedFilmName)
	cleanedFilmName = re.sub(u"[çÇ]", "c", cleanedFilmName)

	filmWords = cleanedFilmName.split(" ")
	url = u"http://www.google.com/search?q=site:traileraddict.com"
	for word in filmWords: 
		url = u"%s+%s" % (url, word)
	request = urllib2.Request(url, None, headers)
	print "Google request: %s" % (url)
	sock = urllib2.urlopen(request)
	parser = URLLister()
	parser.feed(sock.read())
	sock.close()
	parser.close()
 
	for url in parser.urls:
		if re.match("^http://www.traileraddict.com/trailer/.*$", url):
			return re.sub("(^http://www.traileraddict.com/trailer/)|(/[A-Za-z0-9\\-]+)", "", url)

	return ""

#print get_trailer_addict_tag("Benjamin Button:%$")

def getText(nodes):
	text = u""
	for node in nodes:
		if node.nodeType == node.CDATA_SECTION_NODE:
			text += node.data
	return text

def getTrailerAddictEmbedded(trailerTag, playerWidth=320):
	url = u"http://api.traileraddict.com/?width=%d&count=1&film=%s" % (playerWidth, trailerTag)
	print "getting trailer addict url: %s" % (url)
	request = urllib2.Request(url, None, headers)
	sock = urllib2.urlopen(request)
	document = xml.dom.minidom.parse(sock)
	return getText(document.getElementsByTagName("embed")[0].childNodes)

def getTrailerAddictEmbeddedPlayer(filmName, playerWidth=320):
	return getTrailerAddictEmbedded(getTrailerAddictTag(filmName), playerWidth)
