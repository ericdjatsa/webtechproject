#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

def cleanName(name):
	return re.sub(u"[^A-Za-z0-9_\\-]", "",
		name.replace(u"ö", "oe").replace(u"ó", "o").replace(u"ò", "o")
		.replace(u"ô", "o").replace(u"õ", "o").replace(u"ø", "o")
		.replace(u"Ö", "Oe").replace(u"Ó", "O").replace(u"Ò", "O")
		.replace(u"Ô", "O").replace(u"Õ", "O").replace(u"Ø", "O")
		.replace(u"ä", "ae").replace(u"á", "a").replace(u"à", "a")
		.replace(u"ã", "a").replace(u"å", "a").replace(u"Ä", "Ae")
		.replace(u"Á", "A").replace(u"À", "A").replace(u"Ã", "A")
		.replace(u"Å", "A").replace(u"ë", "e").replace(u"é", "e")
		.replace(u"è", "e").replace(u"ê", "e").replace(u"ẽ", "e")
		.replace(u"Ë", "E").replace(u"É", "E").replace(u"È", "E")
		.replace(u"Ê", "E").replace(u"Ẽ", "E").replace(u"ï", "i")
		.replace(u"í", "i").replace(u"ì", "i").replace(u"î", "i")
		.replace(u"ĩ", "i").replace(u"Ï", "I").replace(u"Í", "I")
		.replace(u"Ì", "I").replace(u"Î", "I").replace(u"Ĩ", "I")
		.replace(u"ü", "ue").replace(u"ú", "u").replace(u"ù", "u")
		.replace(u"û", "u").replace(u"ũ", "u").replace(u"Ü", "Ue")
		.replace(u"Ú", "U").replace(u"Ù", "U").replace(u"Û", "U")
		.replace(u"Ũ", "U").replace(u"ç", "c").replace(u"Ç", "C")
		.replace(u"ß", "ss").replace(u"œ", "oe").replace(u"Œ", "Oe")
		.replace(u"æ", "ae").replace(u"Æ", "Ae").replace(u"ñ", "n")
		.replace(u"Ñ", "N").replace(u" ", "_").replace(u"Œ", "Oe"))
