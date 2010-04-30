from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader

import logging
import datetime

from src.seeker.workflows import *
from django.utils.simplejson import JSONDecoder, JSONEncoder

def do_general_search(request):
    wf = General_Search_WF(request.POST, None)
    result = wf.work()
    return render_to_response("template_targeted", result)
    
def do_specific_search(request):
    wf = Specific_Search_WF(request.POST, None)
    result = wf.work()
    return render_to_response("template targeted", result)

def create_fake_actor(request):
    logging.Logger.debug("hello")
    wf = Fake_Actor_Builder({"first-name" : "john",
                             "last-name" : "doe",
                             "birth-date" : datetime.date.today()
                            }, None)
    result = wf.work()
    return HttpResponse(result["status"])

def index(request):
    return render_to_response('seeker/base.html')
