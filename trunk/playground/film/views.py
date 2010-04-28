# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from imdb import IMDb

from playground.film.models import DiskScanResult

def add_to_db(request):
	diskScanResult  = DiskScanResult.objects.all()
	#ignoredFiles = IgnoreFilms.objects().all()
	imdb = IMDb(accessSystem='http', adultSearch=0)
	imdbMatches = {}

	#TODO subtract films from ignore list here
	
	imdb.set_proxy('')

	for result in diskScanResult:
		imdbResultSet = imdb.search_movie(result.filename)[:5]
		imdbMatches[result.filename] = []
		for imdbResult in imdbResultSet:
#movie = imdb.get_movie(imdbResult)
			imdbMatches[result.filename].append(imdbResult)
		

	template = loader.get_template('film/add_to_db.html')
	context = Context({
		'disk_scan_result': diskScanResult,
		'imdb_matches': imdbMatches,
	})
	return HttpResponse(template.render(context))

#default page which is shown when no action is taken
#def index(request):
#	#get a list of latest 20 messages ordered by timestamp
#    latest_message_list = Message.objects.all().order_by('-timestamp')[:20]
#	#get the view for this page
#    t = loader.get_template('sandbox/index.html')
#    c = Context({
#        'latest_message_list': latest_message_list,
#    })
#   return HttpResponse(t.render(c))


#def post(request):
#	try:
#		#first check if post data was provided. If not, this fails with a KeyError,
#		#and we fall back to the except below
#		title = request.POST['title']
#		text = request.POST['text']
#		#create message object
#		msg = Message(title = title, text = text)
#		#save it to the database
#		msg.save()		
#		#redirect to front page
#		return HttpResponseRedirect(reverse('playground.sandbox.views.index'))
#	except (KeyError):
#		#show post message page
#		t = loader.get_template('sandbox/post.html')
#		c = Context()
#		return HttpResponse(t.render(c))
#
#def message(request, msg_id):
#	#show a message referenced by its id
#	msg = get_object_or_404(Message, pk=msg_id)
#	t = loader.get_template('sandbox/message.html')
#	c = Context({'message': msg,})
#	return HttpResponse(t.render(c))
