# -*- coding: utf-8 -*-
from src.crawler.models import File
from src.utils.imdb_cache import imdbSearchMovie
from src.utils.imdb_cache import imdbUpdate
from src.frontend.models import Movie
from src.frontend.models import IgnoreTable
from src.frontend.models import Trailer
from src.frontend.models import Genre
from src.frontend.models import ActedIn
from src.frontend.models import Directed
from src.frontend.models import Wrote
from src.frontend.models import Person
from src.frontend.models import Character
from src.frontend.models import get_or_create_character
from src.frontend.models import get_or_create_person
from src.frontend.models import get_or_create_genre
from src.utils.internet_movie_archive import get_trailer_embed
#from src.storage.store_movie import Store_movie

#get all files which are not in the ignore table or in the movie table from the crawler table. This query
#uses raw sql because django is stupid and not capable of doing this query (as opposed to rubyOnRails),
#and might easily be broken by changing table names, so please do not do this!!!!
def getNewCrawledFiles():
#	return File.objects.extra( where=["(not exists (select * from frontend_ignoretable where frontend_ignoretable.filename = crawler_file.filename and frontend_ignoretable.md5 = crawler_file.hash_code) and not exists (select * from seeker_movie_model where seeker_movie_model.hash_code = crawler_file.hash_code and seeker_movie_model.filename = crawler_file.filename))"])
  return File.objects.extra( where=["(not exists (select * from frontend_ignoretable where frontend_ignoretable.filename = crawler_file.filename and frontend_ignoretable.hash_code = crawler_file.hash_code) and not exists (select * from frontend_movie where frontend_movie.hash_code = crawler_file.hash_code and frontend_movie.filename = crawler_file.filename))"])

def queryImdbWithCrawledFiles():
	diskScanResult  = getNewCrawledFiles()
	imdbMatches = {}
	for file in File.objects.all():
		imdbMatches[file.id] = imdbSearchMovie(file.filename)
	return (diskScanResult, imdbMatches)

def dictGet(dict, key, defaultValue = u""):
	if dict.has_key(key):
		return dict[key]
	else:
		return defaultValue

def getImdbMovie(imdbMovies, imdbId):
	for m in imdbMovies:
		if m.getID() == imdbId:
			return m
	raise Exception ("movie not found") 

def saveMovie(mov, file):
	m = Movie(
		title = dictGet(mov, 'title')[:(Movie._meta.get_field('title').max_length - 2)],
		year = dictGet(mov, 'year'),
		image_url = dictGet(mov, 'cover url')[:(Movie._meta.get_field('image_url').max_length - 2)],
		filename = file.filename[:(Movie._meta.get_field('filename').max_length - 2)],
		extension = file.extension[:(Movie._meta.get_field('extension').max_length - 2)],
		hash_code = file.hash_code[:(Movie._meta.get_field('hash_code').max_length - 2)],
		path = file.path[:(Movie._meta.get_field('path').max_length - 2)],
		imdb_id = mov.getID()[:(Movie._meta.get_field('imdb_id').max_length - 2)],
		plot = dictGet(mov, 'plot', [""])[0].split("::")[0],
		short_plot = dictGet(mov, 'plot outline'),
		is_full = True,
		runtimes = dictGet(mov, 'runtimes', [0])[0][:(Movie._meta.get_field('runtimes').max_length - 2)],
		rating = dictGet(mov, 'rating', 0.0))
	try:
		m.save()
	except Exception, e:
		print e
		
	for genre in dictGet(mov, 'genre', []):
		g = get_or_create_genre(genre)
		try:
			g.save()
			m.genres.add(g)
		except Exception, e:
			print e
		
	for actor in dictGet(mov, 'actors', []):
#		actor = imdbUpdate(actor)
		p = get_or_create_person(name = dictGet(actor, 'name'),
			imdb_id = actor.getID())
		q = get_or_create_character(name = dictGet(actor.currentRole, 'name'),
			imdb_id = actor.currentRole.getID())
		r= ActedIn(
			actor = p,
			character = q,
			movie = m)
		try:
			r.save()
		except Exception, e:
			print e
	
	for writer in dictGet(mov, 'writer', []):
		p = get_or_create_person(name = dictGet(writer, 'name'),
			imdb_id = writer.getID())
		r = Wrote(
			person = p,
			movie = m)
		try:
			r.save()
		except Exception, e:
			print e
		
	for director in dictGet(mov, 'director', []):
		get_or_create_person(name = dictGet(director, 'name'),
			imdb_id = director.getID())
		r = Directed(
			person = p,
			movie = m)
		try:
			r.save()
		except Exception, e:
			print e
		

def addFilmsToDb(diskScanResult, imdbMatches, association):
	for d in diskScanResult:
		try:
			assoc = association["%d" % (d.id)]
			if assoc == 'ignore':
				print "putting file %s in ignore table" % (d.path)
				IgnoreTable(filename = d.filename, hash_code = d.hash_code, extension = d.extension, path = d.path).save()
			else:
				#TODO: Add movie to database (query christophe about that)
				#search imdb movie for this id
				imdbMovie = getImdbMovie(imdbMatches[d.id], assoc)
				print "putting file %s as film %s in film table" % (d.path, dictGet(imdbMovie, 'title'))
				saveMovie(imdbMovie, d)
#				Store_movie(movie = imdbMovie, fichier = d).start()
				#making imdb_id primary key is not enough to do away with this if, as get_trailer_embed 
				#will still be called, which is exactly the overhead we're trying to avoid using the DB. 
				if Trailer.objects.filter(imdb_id = imdbMovie.getID()).__len__() == 0:
					Trailer(imdb_id = imdbMovie.getID(), trailer_url = get_trailer_embed(imdbMovie.getID())).save()
#		except Exception as ex:
		except Exception, ex:
			print ex



		
	
