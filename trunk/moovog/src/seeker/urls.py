'''
Created on 19 avr. 2010

@author: Christophe
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$','src.seeker.views.index'),
                       (r'^__fake-actor/$','src.seeker.views.create_fake_actor'),
                       (r'^general-search/$','src.seeker.views.do_general_search'),
                       (r'^create-actor/$','src.seeker.views.create_actor'),
)