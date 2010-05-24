# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response

from src.frontend.add_to_db import * 
from src.frontend.models import Film
from src.seeker.models import Movie_Model

def index(request):
	return HttpResponse(loader.get_template('frontend/film_list.html').render(Context({
		'movies' : Movie_Model.objects.all(), 
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
		try:
			addFilmsToDb(request.session['disk_scan_result'], request.session['imdb_matches'], request.POST)
			for k in request.POST.keys():
				print "POST %s: %s" % (k, request.POST[k])
		except:
			#TODO show error message
			pass
		finally:
			return HttpResponseRedirect(reverse('src.frontend.views.index'))		
	else:
		return HttpResponseRedirect(reverse('src.frontend.views.index'))		

def preferences(request):
	 return HttpResponse(loader.get_template('frontend/preferences.html').render(Context({})))