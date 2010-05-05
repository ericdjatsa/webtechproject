from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

import logging
import datetime

from src.seeker.workflows import *
from django.utils.simplejson import JSONDecoder, JSONEncoder

def index(request):
    return render_to_response('seeker/base.html', {})

def search(request):
    if request.method == "GET": HttpResponse("POST excepted")
    wf = General_Search_WF(request.POST, None)
    result = wf.work()
    return render_to_response("template_targeted", result)

def create_actor(request):
    if request.method == "GET": HttpResponse("POST excepted")
    wf = Fake_Actor_Builder(request.POST, None)
    result = wf.work()
    return HttpResponse(result["status"])

def create_movie_completely(request):
    """
        This view requires of course a giant HTTP POST request to work.
        It's been gracefully written by Christophe (me ^^) to ease your
        efforts to feed seeker's models.
        Of course also, you can use a smoother method, which consist in
        building progressively the movie model, than the other models,
        then combine them together.
    
        INPUT :
            RELATED TO THE CURRENT MOVIE :
                original-title
                runtime
                user-rating
                thumbnail
                filename
                extension
                path
                md5
            RELATED TO COUNTRIES :
                [country-name] : list of country names
            RELATED TO AWARDS :
                [award-category-name] : list of award category names
                award-name
                date-of-awarding
                award-status
            RELATED TO CHARACTERS :
                character-name
                actor-name
            RELATED TO ACTORS :
                {first-name, last-name, birth-date, nick-name (None if None),
                death-date (None if None), {[award-category-name],
                award-name, date-of-awarding, award-status}}
            RELATED TO WRITERS :
                {first-name, last-name, birth-date, nick-name (None if None),
                death-date (None if None), {[award-category-name],
                award-name, date-of-awarding, award-status}}
            RELATED TO DIRECTORS :
                {first-name, last-name, birth-date, nick-name (None if None),
                death-date (None if None), {[award-category-name],
                award-name, date-of-awarding, award-status}}
            RELATED TO GENRES :
                [genre-name] : list of genre names
            RELATED TO AKAS :
                aka-name
                [country-name] : list of country names
            RELATED TO RELEASE DATES :
                {release-date-1 : [country-name-1, country-names-2, ...], ...}
            RELATED TO SYNOPSISES :
                {plain-text-1 : [country-name-1, country-names-2, ...], ...}
    """
    if request.method == "GET": HttpResponse("POST excepted")
    wf_start_movie = Create_Or_Get_Movie_WF(request.POST, None)
    result_start_movie = wf_start_movie.work()
    request.POST["movie-id"] = result_start_movie["movie-id"]
    