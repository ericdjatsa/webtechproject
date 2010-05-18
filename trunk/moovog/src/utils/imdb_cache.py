from imdb import IMDb
from src.frontend.models import ImdbCache
import cPickle
import base64

#maximum number of search results from imdb to consider
maxResults = 5

def imdbSearchMovie(title):
	cached = ImdbCache.objects.filter(keyword = title).order_by('result_index')
	if cached.__len__() > 0:
		resultList = []		
		for c in cached:
			content = base64.b64decode(c.content)
			resultList.append(cPickle.loads(content))
		return resultList
	else:
		imdb = IMDb()
		resultList = imdb.search_movie(title)[:maxResults]
		i = 0
		for result in resultList:
			imdb.update(result)
			content = base64.b64encode(cPickle.dumps(result, 2))
			c = ImdbCache(keyword = title, result_index = i, imdb_id = result.getID(), content = content)
			c.save()
			i = i + 1
		return resultList
