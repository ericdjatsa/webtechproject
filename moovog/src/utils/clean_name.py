#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

def cleanName(name):
	cleanedName = re.sub(u"[:/!#\\$%&\\(\\)\\-\\+\\.\\?\\/'\"]", "", name)
	cleanedName = re.sub(u"[öóòóøôõÖÒÓÔÕÖØ]", "o", cleanedName)
	cleanedName = re.sub(u"[àáâåãäÀÁÂÅÃÄ]", "a", cleanedName)
	cleanedName = re.sub(u"[èéêẽëÈÉÊẼË]", "e", cleanedName)
	cleanedName = re.sub(u"[ìíîĩïÌÍÎĨÏ]", "i", cleanedName)
	cleanedName = re.sub(u"[ùúûũüÙÚÛÜŨ]", "u", cleanedName)
	cleanedName = re.sub(u"[çÇ]", "c", cleanedName)
	cleanedName = re.sub(u"[ß]", "ss", cleanedName)
	cleanedName = re.sub(u"[œŒ]", "oe", cleanedName)
	cleanedName = re.sub(u"[æÆ]", "ae", cleanedName)
	cleanedName = re.sub(u"[ñÑ]", "n", cleanedName)
	return cleanedName
