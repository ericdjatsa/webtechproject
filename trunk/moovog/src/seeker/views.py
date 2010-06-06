# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from random import sample

from src.frontend.add_to_db import *
#from src.frontend.models import Movie
from src.utils.clean_name import cleanName
from src.utils.imdb_cache import imdbUpdate
from src.utils.imdb_cache import imdbGetPerson
from src.utils.get_image import getOrCacheImage

import logging
from datetime import datetime

from src.seeker.workflows import *
from django.utils.simplejson import JSONDecoder, JSONEncoder

from src.seeker.models import *

def seeker_test_index(request):
    return render_to_response("seeker/seeker_base.html", {})

def index(request):
    return HttpResponse(loader.get_template('frontend/film_list.html').render(Context({
        'movies' : Movie_Model.objects.all(), 
        'paginate_by' : 5,})))

def search(request):
    """
        INPUT :
            search-string
            search-option
        OUTPUT :
            Search_WF's OUTPUT
            time-to-serve
    """
    start = datetime.now()
    search_wf = Search_WF(request.GET, None)
    search_result = search_wf.work()
    
    search_type = request.GET["search-option"]
    search_words = request.GET["search-string"]
    
    if search_type in ["movie-original-title", "movie-aka-title"]:
        template = loader.get_template('frontend/search_movie.html')
    elif search_type in ["actor", "writer", "director"]:
        template = loader.get_template('frontend/search_person.html')
    elif search_type == "character":
        template = loader.get_template('frontend/search_character.html')
    elif search_type == "genre":
        template = loader.get_template('frontend/search_genre.html')
    elif search_type == "award":
        template = loader.get_template('TO DO : frontend/search_award.html')
    elif search_type == "award-category":
        template = loader.get_template('TO DO : frontend/search_award_category.html')
    
    if len(search_result["search-result"]) == 1:
            if search_type in ["movie-original-title", "movie-aka-title"]:
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.movie', args= (cleanName(search_result["search-result"][0].original_title), search_result["search-result"][0].id)))
            elif search_type == "actor":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.actor', args= (cleanName(search_result["search-result"][0].full_name), search_result["search-result"][0].id)))
            elif search_type == "director":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.director', args= (cleanName(search_result["search-result"][0].full_name), search_result["search-result"][0].id)))
            elif search_type == "writer":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.writer', args= (cleanName(search_result["search-result"][0].full_name), search_result["search-result"][0].id)))
            elif search_type == "character":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.character', args= (cleanName(search_result["search-result"][0].character_name), search_result["search-result"][0].id)))
            elif search_type == "genre":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.genre', args= (cleanName(search_result["search-result"][0].genre_name), search_result["search-result"][0].id)))
            elif search_type == "award":
                pass
            elif search_type == "award_category":
                pass
    
#    display_result = {}
#    if search_result["type-of-result"] == "homogeneous":
#        homogeneous_wf = Get_Infos_For_Homogeneous_Search_WF(
#                        {"dict-of-models" : search_result["search-result"]}, None)
#        display_result = homogeneous_wf.work()
#    if search_result["type-of-result"] == "heterogeneous":
#        heterogeneous_wf = Get_Infos_For_Heterogeneous_Search_WF(
#                            {"dict-of-matches" : search_result["search-result"]}, None)
#        display_result = heterogeneous_wf.work()
    served_in = datetime.now() - start + search_result["time-to-serve"]
    search_result["time-to-serve"] = str(served_in.microseconds)
#    return render_to_response("template_targeted", result)
#    return HttpResponse(JSONEncoder().encode(str(search_result["search-result"]["actor-models"][0].get_infos_for_model())))
#    return HttpResponse(JSONEncoder().encode(str(display_result["result"])))
    context = Context({'results': search_result["search-result"],
                       'type' : search_type,
                       'query': search_words,
                       'time' : search_result["time-to-serve"]})
    return HttpResponse(template.render(context))

def get_detailed_infos_for_movie(request):
    """
        INPUT :
            movie-id
        OUTPUT :
            Get_Detailed_Infos_For_Movie_Model_WF's output
    """
    start = datetime.now()
    if request.method == "GET": HttpResponse("POST excepted")
    details_wf = Get_Detailed_Infos_For_Movie_Model_WF(request.POST, None)
    result = details_wf.work()
    result["time-to-serve"] += datetime.now() - start
    
#    return render_to_response("template_url", JSONEncoder().encode(str(result)))
    return HttpResponse(JSONEncoder().encode(str(result)))

def get_detailed_infos_for_person(request):
    """
        INPUT :
            person-id
            person-type
        OUTPUT :
            Get_Detailed_Infos_For_Person_Model_WF's output
    """
    start = datetime.now()
    if request.method == "GET": HttpResponse("POST excepted")
    details_wf = Get_Detailed_Infos_For_Person_Model_WF(request.POST, None)
    result = details_wf.work()
    result["time-to-serve"] += datetime.now() - start
    
#    return render_to_response("template_url", JSONEncoder().encode(str(result)))
    return HttpResponse(JSONEncoder().encode(str(result)))

def create_fake_complete_movie(request):
    """
        INPUT :
            None
        OUTPUT :
            Create_Fake_Movie_WF's 
    """
    wf = Create_Fake_Movie_WF({}, None)
    result = wf.work()
    return HttpResponse(JSONEncoder().encode(", ".join([result["status"],
                                            str(result["already-existed"]),
                                            str(result["time-to-serve"])])))

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
        addFilmsToDb(request.session['disk_scan_result'], request.session['imdb_matches'], request.POST)
        return HttpResponseRedirect(reverse('src.seeker.views.index'))
    else:
        return HttpResponseRedirect(reverse('src.seeker.views.index'))        
    
def preferences(request):
     return HttpResponse(loader.get_template('frontend/preferences.html').render(Context({})))
     
def movie(request, name, movie_id):
    m = get_object_or_404(Movie_Model, id = movie_id)
#    m = Movie_Model.objects.filter(id = movie_id)
    randomIds = sample(xrange(1, Movie_Model.objects.count()), 8)
    randomMovies = Movie_Model.objects.filter(id__in = randomIds)[:5]
#    randomMovies = Movie.objects.filter(id = 1)
    template = loader.get_template('frontend/movie.html')
    context = Context({'movie': m, 'random_movies': randomMovies,
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
    
#def person(request, name, person_id):
#    p = get_object_or_404(Person, id = person_id)
#    fetch_person(p)
#    template = loader.get_template('frontend/person.html')
#    context = Context({
#        'person': p,
#        'directed': Directed.objects.filter(person = p),
#        'acted': ActedIn.objects.filter(actor = p),
#        'wrote': Wrote.objects.filter(person = p),
#        })
#    return HttpResponse(template.render(context))

def actor(request, name, person_id):
    p = get_object_or_404(Actor_Model, id = person_id)
    template = loader.get_template('frontend/person.html')
    context = Context({'person': p, 'type' : 'actor'})
    return HttpResponse(template.render(context))

def director(request, name, person_id):
    p = get_object_or_404(Director_Model, id = person_id)
    template = loader.get_template('frontend/person.html')
    context = Context({'person': p, 'type' : 'director'})
    return HttpResponse(template.render(context))

def writer(request, name, person_id):
    p = get_object_or_404(Writer_Model, id = person_id)
    template = loader.get_template('frontend/person.html')
    context = Context({'person': p, 'type' : 'writer'})
    return HttpResponse(template.render(context))
    
def character(request, name, character_id):
    c = get_object_or_404(Character_Model, id = character_id)
    template = loader.get_template('frontend/character.html')
    context = Context({
        'character': c,
        'movies': Movie_Model.objects.filter(character_model = c),
        })
    return HttpResponse(template.render(context))
    
def genre(request, name, genre_id):
    print "Getting genre %s" % str(genre_id)
    g = get_object_or_404(Genre_Model, id = genre_id)
    template = loader.get_template('frontend/genre.html')
    context = Context({'genre': g})
    return HttpResponse(template.render(context))
    
def movie_watch(request, name, movie_id):
    m = get_object_or_404(Movie_Model, pk = movie_id)
    template = loader.get_template('frontend/movie_watch.html')
    context = Context({'movie': m})
    return HttpResponse(template.render(context))
    
def search_post(request):
#    try:    
        search_type = request.GET["search-option"]
        search_words = request.GET["search-string"]
        
        if search_type == "person":
            template = loader.get_template('frontend/search_person.html')
            results = Actor_Model.objects.all()
        elif search_type == "character":
            template = loader.get_template('frontend/search_character.html')
            results = Character_Model.objects.all()
        elif search_type == "genre":
            template = loader.get_template('frontend/search_genre.html')
            results = Genre_Model.objects.all()
        elif search_type in ["movie-original-title", "movie-aka-title"]:
            template = loader.get_template('frontend/search_movie.html')
            results = Movie_Model.objects.all()
        
        for word in search_words.split(" "):
            if search_type in ["movie-original-title", "movie-aka-title"]:
                results = results.filter(original_title__icontains = word)
            elif search_type in ["actor", "writer", "director"]:
                results = results.filter(full_name__icontains = word)
            elif search_type == "character":
                results = results.filter(character_name__icontains = word)
            elif search_type == "genre":
                results = results.filter(genre_name__icontains = word)
            
        if results.__len__() == 1:
            if search_type == "movie":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.movie', args= (cleanName(results[0].original_title), results[0].id)))
            elif search_type == "person":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.person', args= (cleanName(results[0].full_name), results[0].id)))
            elif search_type == "character":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.character', args= (cleanName(results[0].character_name), results[0].id)))
            elif search_type == "genre":
                return HttpResponseRedirect(reverse(viewname='src.seeker.views.genre', args= (cleanName(results[0].genre_name), results[0].id)))
        
        context = Context({'results': results, 'query': search_words})
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
        string_list = query.split(" ")
        
        if qtype == "actor":
            results = Actor_Model.objects.all()
        elif qtype == "writer":
            results = Writer_Model.objects.all()
        elif qtype == "director":
            results = Director_Model.objects.all()
        elif qtype == "character":
            results = Character_Model.objects.all()
        elif qtype == "genre":
            results = Genre_Model.objects.all()
        elif qtype in ["movie-original-title", "movie-aka-title"]:
            results = Movie_Model.objects.all()
            
        for word in string_list:
            if qtype in ["movie-original-title", "movie-aka-title"]:
                results = results.filter(original_title__icontains = word)
                result_strings = [ {'name': r.original_title, 'img': r.thumbnail_url} for r in results[:limit]]
            elif qtype in ["actor", "writer", "director"]:
                results = results.filter(full_name__icontains = word)
                result_strings = [ {'name': r.full_name, 'img': r.thumbnail_url} for r in results[:limit]]
            elif qtype == "character":
                results = results.filter(character_name__icontains = word)
                # , 'img': r.thumbnail_url to character...
                result_strings = [ {'name': r.character_name, 'img': ""} for r in results[:limit]]
            elif qtype == "genre":
                results = results.filter(genre_name__icontains = word)
                result_strings = [ {'name': r.genre_name, 'img': ""} for r in results[:limit]]
            
        data = ""
        for r in result_strings:
            data = data + r['name'];
            if qtype in ["movie-original-title", "movie-aka-title", "actor", "writer", "director", "character"]:
                image = getOrCacheImage(r['img'])
                if not (image == None or image == ""): 
                    data = data + "&" + image
            data = data + "\n"
            
#        data = simplejson.dumps({'message': {'type': 'debug', 'msg': 'no error'}, 'data': result_strings})
#        data = serializers.serialize('json', {'message': {'type': 'debug', 'msg': 'no error'}, 'data': result_strings})
        print data
#        return HttpResponse(serializers.serialize('json', {'error': 'none', 'data': result_strings}), mimetype='application/json')
#        return HttpResponse(serializers.serialize('json', result_strings), mimetype='application/json')
#        return HttpResponse(json, mimetype='application/json')
        return HttpResponse(content = data, mimetype='text/plain; encoding=UTF-8')