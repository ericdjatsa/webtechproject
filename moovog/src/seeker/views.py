# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

import logging
from datetime import datetime

from src.seeker.workflows import *
from django.utils.simplejson import JSONDecoder, JSONEncoder

def index(request):
    return render_to_response("seeker/base.html", {})

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
    if request.method == "GET": HttpResponse("POST excepted")
    search_wf = Search_WF(request.POST, None)
    search_result = search_wf.work()
    
    display_result = {}
    if search_result["type-of-result"] == "homogeneous":
        homogeneous_wf = Get_Infos_For_Homogeneous_Search_WF(
                        {"dict-of-models" : search_result["search-result"]}, None)
        display_result = homogeneous_wf.work()
#    if search_result["type-of-result"] == "heterogeneous":
#        heterogeneous_wf = Get_Infos_For_Heterogeneous_Search_WF(
#                            {"dict-of-matches" : search_result["search-result"]}, None)
#        display_result = heterogeneous_wf.work()
    
    display_result["result"]["time-to-serve"] = str(datetime.now() - start
                                                + search_result["time-to-serve"]
                                                + display_result["time-to-serve"])
#    return render_to_response("template_targeted", result)
#    return HttpResponse(JSONEncoder().encode(str(search_result["search-result"]["actor-models"][0].get_infos_for_model())))
    return HttpResponse(JSONEncoder().encode(str(display_result["result"])))

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

def test_area(request):
    """
        playground fur mich ! ^^
    """
    movie = Movie_Model.get_movie_model_by_id(1)
    return HttpResponse(str(movie.get_infos_for_model()))