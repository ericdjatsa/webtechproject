# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from imdb import IMDb

from src.frontend.models import Film
from src.crawler.models import File

def add_to_db(request):
	diskScanResult  = File.objects.all()
#	#ignoredFiles = IgnoreFilms.objects().all()
	imdb = IMDb(accessSystem='http', adultSearch=0)
	imdbMatches = {}
#	threadPool = ThreadPool(5)
#
#
#	#TODO subtract films from ignore list here
#	
	imdb.set_proxy('')
#
##	def parallelQueryImdbDetails(movie):
#		imdb.update(movie)
#		return 0
#
#	def parallelQueryImdbMovie(movieName):
#		movies = imdb.search_movie(movieName)[:5]
#		requests = makeRequests(parallelQueryImdbDetails, movies)
#		[threadPool.putRequest(request) for request in requests]
#		pool.wait()
#		return movies
#
#	def parallelQueryImdbMovies(movies)
#		requests = makeRequests(parallelQueryImdbMovie, movies)
#		[threadPool.putRequest(request) for request in requests]
#		pool.wait()
#		return 
		 


	for result in diskScanResult:
		print "Searching movie %s" % (result.filename)
		imdbResultSet = imdb.search_movie(result.filename)[:5]
		imdbMatches[result.filename] = []
		firstResult = 1
		for imdbResult in imdbResultSet:
			#update only first of found movies to contain all data, as data retrieval takes a long time
#			if firstResult:
#				firstResult = 0
			imdb.update(imdbResult)
			imdbMatches[result.filename].append(imdbResult)
			print "Found movie %s" % (imdbResult["title"])
		try: 
			title = imdbResultSet[0]['title'] 
		except: 
			title = ''
		try: 
			year = imdbResultSet[0]['year'] 
		except: 
			year = 1880
		try: 
			image = imdbResultSet[0]['cover url']
		except: 
			image = ''
		m = Film(title=title, release_date = datetime(year = year, month=1, day=1), image = image)
		try: 
			m.save() 
		except: 
			pass
	

	template = loader.get_template('frontend/add_to_db.html')
	context = Context({
#		'disk_scan_result': diskScanResult,
#		'imdb_matches': imdbMatches,
	})
	return HttpResponse(template.render(context))

