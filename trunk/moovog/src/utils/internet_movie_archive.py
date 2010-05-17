#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import xml.dom.minidom

developer_id = u"09e7f0a9-fe7f-430d-8b55-e66def4f3f4d" #developer id for internet movie archive api
id_type = 12 #id type imdb
headers = {u'User-Agent': u'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/6.0'}

def getText(nodes):
	text = u""
	for node in nodes:
		if node.nodeType == node.CDATA_SECTION_NODE:
			text += node.data
	return text

def get_trailer_embed(imdb_id):
	url = u"http://api.internetvideoarchive.com/Video/PinPoint.aspx?DeveloperId=%s&IdType=%d&SearchTerm=%s" % (developer_id, id_type, imdb_id)
	print "getting internet movie archive url: %s" % (url)
	request = urllib2.Request(url, None, headers)
	sock = urllib2.urlopen(request)
	document = xml.dom.minidom.parse(sock)
	try:
		return getText(document.getElementsByTagName("EmbedUrl")[0].childNodes)
	except:
		return u""

