import os
import re
import settings
from urllib import urlretrieve

localImageDirectory = "%s/image/thumbnails" % (settings.STATIC_DOC_ROOT)
localImageUrlTemplate = "/static/image/thumbnails"

def imageName(imdb_url):
	return re.split('/', imdb_url)[-1]

def localImagePath(imdb_url):
	return "%s/%s" % (localImageDirectory, imageName(imdb_url))

def localImageUrl(imdb_url):
	return "%s/%s"% (localImageUrlTemplate, imageName(imdb_url))

def isImageAlreadyStored(imdb_url):
	return os.path.isfile(localImagePath(imdb_url))

def downloadImage(imdb_url):
	urlretrieve(imdb_url, localImagePath(imdb_url))
	

def getOrCacheImage(imdb_url):
	if not isImageAlreadyStored(imdb_url):
		downloadImage(imdb_url)
	return localImageUrl(imdb_url)
		
	
