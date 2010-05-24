# -*- coding: utf-8 -*-
from src.crawler.models import File
from src.utils.imdb_cache import imdbSearchMovie
from imdb import IMDb
from src.frontend.models import Film
from src.frontend.models import IgnoreTable
from src.frontend.models import Trailer
from src.utils.internet_movie_archive import get_trailer_embed
from src.storage.store_movie import Store_movie

imdb = IMDb(accessSystem='http', adultSearch=0)
imdb.set_proxy('')

#get all files which are not in the ignore table or in the movie table from the crawler table. This query
#uses raw sql because django is stupid and not capable of doing this query (as opposed to rubyOnRails),
#and might easily be broken by changing table names, so please do not do this!!!!
def getNewCrawledFiles():
#	return File.objects.extra( where=["(not exists (select * from frontend_ignoretable where frontend_ignoretable.filename = crawler_file.filename and frontend_ignoretable.md5 = crawler_file.hash_code) and not exists (select * from seeker_movie_model where seeker_movie_model.hash_code = crawler_file.hash_code and seeker_movie_model.filename = crawler_file.filename))"])
  return File.objects.extra( where=["(not exists (select * from frontend_ignoretable where frontend_ignoretable.filename = crawler_file.filename and frontend_ignoretable.md5 = crawler_file.hash_code) and not exists (select * from frontend_film where frontend_film.hash_code = crawler_file.hash_code and frontend_film.filename = crawler_file.filename))"])

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

def addFilmsToDb(diskScanResult, imdbMatches, association):
	for d in diskScanResult:
		try:
			assoc = association["%d" % (d.id)]
			if assoc == 'ignore':
				print "putting file %s in ignore table" % (d.path)
				IgnoreTable(filename = d.filename, md5 = d.hash_code, extension = d.extension, path = d.path).save()
			else:
				#TODO: Add movie to database (query christophe about that)
				#search imdb movie for this id
				imdbMovie = getImdbMovie(imdbMatches[d.id], assoc)
				print "putting file %s as film %s in film table" % (d.path, dictGet(imdbMovie, 'title'))
				Film(title = dictGet(imdbMovie, 'title'), image = dictGet(imdbMovie, 'cover url'), 
				  year = dictGet(imdbMovie, 'year'), filename = d.filename, extension = d.extension,
				  hash_code = d.hash_code, path = d.path, imdb_id = imdbMovie.getID()).save()
				Store_movie(movie = imdbMovie, fichier = d).start()
				#making imdb_id primary key is not enough to do away with this if, as get_trailer_embed 
				#will still be called, which is exactly the overhead we're trying to avoid using the DB. 
				if Trailer.objects.filter(imdb_id = imdbMovie.getID()).__len__ == 0:
				  Trailer(imdb_id = imdbMovie.getID(), trailer_url = get_trailer_embed(imdbMovie.getID())).save()
		except Exception as ex:
			print ex



		
	
