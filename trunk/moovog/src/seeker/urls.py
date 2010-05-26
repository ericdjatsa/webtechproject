'''
Created on 19 avr. 2010

@author: Christophe
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$','src.seeker.views.index'),
                       (r'^__fake/complete-movie-creation/$','src.seeker.views.create_fake_complete_movie'),
                       (r'^search/$','src.seeker.views.search'),
                       (r'^get-detailed-movie-infos/$','src.seeker.views.get_detailed_infos_for_movie'),
                       (r'^get-detailed-person-infos/$','src.seeker.views.get_detailed_infos_for_person'),
                       (r'^__test/$','src.seeker.views.test_area'),
)
