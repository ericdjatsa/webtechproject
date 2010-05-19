'''
Created on 19 avr. 2010

@author: Christophe
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$','src.seeker.views.index'),
                       (r'^__fake/complete-movie-creation/$','src.seeker.views.create_fake_complete_movie'),
                       (r'^search/$','src.seeker.views.search'),
                       (r'^__test/$','src.seeker.views.test_area'),
)
