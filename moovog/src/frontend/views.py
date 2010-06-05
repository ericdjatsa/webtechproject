# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from random import sample

from src.frontend.add_to_db import * 
from src.frontend.models import Movie
from src.utils.clean_name import cleanName
from src.utils.imdb_cache import imdbUpdate
from src.utils.imdb_cache import imdbGetPerson
#from src.seeker.models import Movie_Model

from src.utils.get_image import getOrCacheImage

def index(request):
	return HttpResponse(loader.get_template('frontend/film_list.html').render(Context({
		'movies' : Movie.objects.all(), 
		'paginate_by' : 5,})))

def add_to_db(request, step):
	if step == '1':
		(diskScanResult, imdbMatches) = queryImdbWithCrawledFiles()
		template = loader.get_template('frontend/add_to_db.html')
		context = Context({
			'disk_scan_result': diskScanResult,
			'imdb_matches': imdbMatches,
		})
		request.session['imdb_matches'] = imdbMatches
		request.session['disk_scan_result'] = diskScanResult
		request.session.set_expiry(0) # delete session on web browser close
		return HttpResponse(template.render(context))
	elif step == '2':
#		try:
			addFilmsToDb(request.session['disk_scan_result'], request.session['imdb_matches'], request.POST)
#		except:
			#TODO show error message
#			pass
#		finally:
			return HttpResponseRedirect(reverse('src.frontend.views.index'))		
	else:
		return HttpResponseRedirect(reverse('src.frontend.views.index'))		
	
def preferences(request):
	 return HttpResponse(loader.get_template('frontend/preferences.html').render(Context({})))
	 
def movie(request, name, movie_id):
	m = get_object_or_404(Movie, id = movie_id)
	randomIds = sample(xrange(1,Movie.objects.count()), 8)
	randomMovies = Movie.objects.filter(id__in = randomIds)[:5]
#	randomMovies = Movie.objects.filter(id = 1)
	template = loader.get_template('frontend/movie.html')
	context = Context({
		'movie': m,
		'directed': Directed.objects.filter(movie = m),
		'acted': ActedIn.objects.filter(movie = m)[:4],
		'wrote': Wrote.objects.filter(movie = m),
		'random_movies': randomMovies
		})
	return HttpResponse(template.render(context))
	
def fetch_person(person):
	if (not person.is_full) and (person.imdb_id != None):
		i = imdbUpdate(imdbGetPerson(person.imdb_id))
		try: person.birth_date = datetime.strptime(i['birth date'], "%d %B %Y").date()
		except: person.birth_date = None
		try: person.death_date = datetime.strptime(i['death date'], "%d %B %Y").date()
		except: person.death_date = None
		try: person.image_url = i['headshot']
		except: person.image_url = None
		try: person.bio = i['mini biography'][0].split("::")[0]
		except: person.bio = None
		try: person.birth_name = i['birth name']
		except: person.birth_name = None
		person.is_full = 1
		person.save()
	
def person(request, name, person_id):
	p = get_object_or_404(Person, id = person_id)
	fetch_person(p)
	template = loader.get_template('frontend/person.html')
	context = Context({
		'person': p,
		'directed': Directed.objects.filter(person = p),
		'acted': ActedIn.objects.filter(actor = p),
		'wrote': Wrote.objects.filter(person = p),
		})
	return HttpResponse(template.render(context))
	
def character(request, name, character_id):
	c = get_object_or_404(Character, id = character_id)
	template = loader.get_template('frontend/character.html')
	context = Context({
		'character': c,
		'movies': ActedIn.objects.filter(character = c),
		})
	return HttpResponse(template.render(context))
	
def genre(request, name, genre_id):
	g = get_object_or_404(Genre, pk = genre_id)
	template = loader.get_template('frontend/genre.html')
	context = Context({
		'genre': g,
		})
	return HttpResponse(template.render(context))
	
def movie_watch(request, name, movie_id):
	m = get_object_or_404(Movie, pk = movie_id)
	template = loader.get_template('frontend/movie_watch.html')
	context = Context({
		'movie': m,
		})
	return HttpResponse(template.render(context))
	
def search_post(request):
#	try:	
		search_type = request.GET["search-option"]
		search_words = request.GET["search-string"]
		
		if search_type == "person":
			template = loader.get_template('frontend/search_person.html')
			results = Person.objects.all()
		elif search_type == "character":
			template = loader.get_template('frontend/search_character.html')
			results = Character.objects.all()
		elif search_type == "genre":
			template = loader.get_template('frontend/search_genre.html')
			results = Genre.objects.all()
		else:
			template = loader.get_template('frontend/search_movie.html')
			results = Movie.objects.all()
		
		for word in search_words.split(" "):
			if search_type == "movie":
				results = results.filter(title__icontains = word)
			else:
				results = results.filter(name__icontains = word)
			
		if results.__len__() == 1:
			if search_type ==  "movie":
				return HttpResponseRedirect(reverse(viewname='src.frontend.views.movie', args= (cleanName(results[0].title), results[0].id)))
			elif search_type == "person":
				return HttpResponseRedirect(reverse(viewname='src.frontend.views.person', args= (cleanName(results[0].name), results[0].id)))
			elif search_type == "character":
				return HttpResponseRedirect(reverse(viewname='src.frontend.views.character', args= (cleanName(results[0].name), results[0].id)))
			elif search_type == "genre":
				return HttpResponseRedirect(reverse(viewname='src.frontend.views.genre', args= (cleanName(results[0].name), results[0].id)))
	
		context = Context({'results': results, 'query': search_words})
		return HttpResponse(template.render(context))
		
def search(request, search_type, search_query):
	print "search called: %s %s" % (search_type, search_query)
	if search_type == "person":
		template = loader.get_template('frontend/search_person.html')
		results = Person.objects.all()
	elif search_type == "character":
		template = loader.get_template('frontend/search_character.html')
		results = Character.objects.all()
	elif search_type == "genre":
		template = loader.get_template('frontend/search_genre.html')
		results = Genre.objects.all()
	else:
		template = loader.get_template('frontend/search_movie.html')
		results = Movie.objects.all()
		
	for word in search_query.split("+"):
		if search_type == "movie":
			results = results.filter(title__icontains = word)
		else:
			results = results.filter(name__icontains = word)
			
	if results.__len__() == 1:
		if search_type ==  "movie":
			return HttpResponseRedirect(reverse(viewname='src.frontend.views.movie', args= (cleanName(results[0].title), results[0].id)))
		elif search_type == "person":
			return HttpResponseRedirect(reverse(viewname='src.frontend.views.person', args= (cleanName(results[0].name), results[0].id)))
		elif search_type == "character":
			return HttpResponseRedirect(reverse(viewname='src.frontend.views.character', args= (cleanName(results[0].name), results[0].id)))
		elif search_type == "genre":
			return HttpResponseRedirect(reverse(viewname='src.frontend.views.genre', args= (cleanName(results[0].name), results[0].id)))
	
	context = Context({'results': results, 'query': search_query.replace("+", " ")})
	return HttpResponse(template.render(context))
	
def search_json(request):
	if not (request.GET.has_key('q') or request.GET.has_key('type')):
		# error handling
		print "Error: request does not have keys q and type: %s" % (request.keys())
		return HttpResponse("", mimetype='text/plain; encoding=UTF-8')
	else:
		query = request.GET['q']
		qtype = request.GET['type']
		limit = (int (request.GET['limit']) if request.GET.has_key('limit') else 5)
		
		
		if qtype == "person":
			results = Person.objects.all()
		elif qtype == "character":
			results = Character.objects.all()
		elif qtype == "genre":
			results = Genre.objects.all()
		else:
			results = Movie.objects.all()
			
		for word in query.split(" "):
			if qtype == "movie":
				results = results.filter(title__icontains = word)
			else:
				results = results.filter(name__icontains = word)
				
		if qtype == "movie":
			result_strings = [ {'name': r.title, 'img': r.image_url} for r in results[:limit]]
		else:
			result_strings = [ {'name': r.name, 'img': r.image_url} for r in results[:limit]]
			
		data = ""
		for r in result_strings:
			data = data + r['name'];
			if qtype == "movie" or qtype == "person":
				image = getOrCacheImage(r['img'])
				if not (image == None or image == ""): 
					data = data + "&" + image
			data = data + "\n"
			
#		data = simplejson.dumps({'message': {'type': 'debug', 'msg': 'no error'}, 'data': result_strings})
#		data = serializers.serialize('json', {'message': {'type': 'debug', 'msg': 'no error'}, 'data': result_strings})
		print data
#		return HttpResponse(serializers.serialize('json', {'error': 'none', 'data': result_strings}), mimetype='application/json')
#		return HttpResponse(serializers.serialize('json', result_strings), mimetype='application/json')
#		return HttpResponse(json, mimetype='application/json')
		return HttpResponse(content = data, mimetype='text/plain; encoding=UTF-8')