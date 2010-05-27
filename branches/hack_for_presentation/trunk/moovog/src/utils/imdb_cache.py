# -*- coding: utf-8 -*-
from imdb import IMDb
import imdb
from src.frontend.models import ImdbCache
from src.frontend.models import ImdbSearch
import cPickle
import base64

#maximum number of search results from imdb to consider
maxResults = 5

def get_imdb_movie_id(imdb_id):
#	return "m%s" % (imdb_id)
	return imdb_id
	
def get_imdb_person_id(imdb_id):
#	return "p%s" % (imdb_id)
	return imdb_id
	
def get_imdb_character_id(imdb_id):
#	return "c%s" % (imdb_id)
	return imdb_id
	
def get_imdb_id(imdb_obj):
	if imdb_obj.__class__ == imdb.Movie.Movie:
		return get_imdb_movie_id(imdb_obj.getID())
	if imdb_obj.__class__ == imdb.Person.Person:
		return get_imdb_person_id(imdb_obj.getID())
	if imdb_obj.__class__ == imdb.Character.Character:
		if imdb_obj.getID() != None:
			return get_imdb_character_id(imdb_obj.getID())

def imdbUpdate(imdb_obj):
	cached = ImdbCache.objects.filter(imdb_id = get_imdb_id(imdb_obj))
	if cached.__len__() > 0 and cached[0].is_full:
		return cPickle.loads(base64.b64decode(cached[0].content))
	else:
		imdb = IMDb()
		imdb.update(imdb_obj)
		content = base64.b64encode(cPickle.dumps(imdb_obj, 2))
		c = ImdbCache(imdb_id = get_imdb_id(imdb_obj), content = content, is_full = True)
		c.save()
		return imdb_obj

def imdbSearchMovie(title):
	cached = ImdbSearch.objects.filter(keyword = title).order_by('result_index')
	if cached.__len__() > 0:
		resultList = []		
		for c in cached:
			content = base64.b64decode(c.imdb_obj.content)
			resultList.append(cPickle.loads(content))
		return resultList
	else:
		imdb = IMDb()
		resultList = imdb.search_movie(title)[:maxResults]
		i = 0
		for result in resultList:
			result = imdbUpdate(result)
			c = ImdbSearch(
				keyword = title, 
				result_index = i, 
				imdb_obj = ImdbCache.objects.filter(imdb_id = get_imdb_id(result))[0])
			c.save()
			i = i + 1
		return resultList
		
def imdbGetMovie(imdb_id):
	cached = ImdbCache.objects.filter(imdb_id = get_imdb_movie_id(imdb_id))
	if cached.__len__() > 0 and cached[0].is_full:
		return cPickle.loads(base64.b64decode(cached[0].content))
	else:
		imdb = IMDb()
		m = imdb.get_movie(imdb_id)
		content = base64.b64encode(cPickle.dumps(m, 2))
		c = ImdbCache(imdb_id = get_imdb_id(m), content = content, is_full = True)
		c.save()
		return m
		
def imdbGetPerson(imdb_id):
	cached = ImdbCache.objects.filter(imdb_id = get_imdb_person_id(imdb_id))
	if cached.__len__() > 0 and cached[0].is_full:
		return cPickle.loads(base64.b64decode(cached[0].content))
	else:
		imdb = IMDb()
		m = imdb.get_person(imdb_id)
		content = base64.b64encode(cPickle.dumps(m, 2))
		c = ImdbCache(imdb_id = get_imdb_id(m), content = content, is_full = True)
		c.save()
		return m		
		
def imdbGetCharacter(imdb_id):
	cached = ImdbCache.objects.filter(imdb_id = get_imdb_character_id(imdb_id))
	if cached.__len__() > 0 and cached[0].is_full:
		return cPickle.loads(base64.b64decode(cached[0].content))
	else:
		imdb = IMDb()
		m = imdb.get_character(imdb_id)
		content = base64.b64encode(cPickle.dumps(m, 2))
		c = ImdbCache(imdb_id = get_imdb_id(m), content = content, is_full = True)
		c.save()
		return m


#def imdbUpdateMovie(movie):
#	cached = ImdbCache.objects.filter(imdb_id = movie.getID())
#	if cached.__len__() > 0:
#		return cPickle.loads(base64.b64decode(cached[0].content))
#	else:
#		imdb = imdb.IMDb()
#           	imdb.update(person)
#		imdb.update(person, info = ['awards'])
#		content = base64.b64encode(cPickle.dumps(person, 2))
#		c = ImdbCache(keyword = '', result_index = 0, imdb_id = person.getID(), content = content)
#		c.save()
#		return person
