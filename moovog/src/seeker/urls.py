'''
Created on 19 avr. 2010

@author: Christophe
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('',
        (r'^$','src.seeker.views.index'),
        (r'^__test_seeker/$','src.seeker.views.seeker_test_index'),
        (r'^__fake/complete-movie-creation/$','src.seeker.views.create_fake_complete_movie'),
        (r'^search/$','src.seeker.views.search'),
        (r'^get-detailed-movie-infos/$','src.seeker.views.get_detailed_infos_for_movie'),
        (r'^get-detailed-person-infos/$','src.seeker.views.get_detailed_infos_for_person'),
        (r'^add_to_db/(?P<step>[1,2])/$', 'src.seeker.views.add_to_db'),
        (r'^movie/(?P<name>[A-Za-z_\-]+)/(?P<movie_id>\d+)/$', 'src.seeker.views.movie'),
        (r'^movie/(?P<name>[A-Za-z_\-]+)/(?P<movie_id>\d+)/watch$', 'src.seeker.views.movie_watch'),
#        (r'^person/(?P<name>[A-Za-z_\-]+)/(?P<person_id>\d+)/$', 'src.seeker.views.person'),
        (r'^actor/(?P<name>[A-Za-z_\-]+)/(?P<person_id>\d+)/$', 'src.seeker.views.actor'),
        (r'^director/(?P<name>[A-Za-z_\-]+)/(?P<person_id>\d+)/$', 'src.seeker.views.director'),
        (r'^writer/(?P<name>[A-Za-z_\-]+)/(?P<person_id>\d+)/$', 'src.seeker.views.writer'),
        (r'^character/(?P<name>[A-Za-z_\-]+)/(?P<character_id>\d+)/$', 'src.seeker.views.character'),
        (r'^genre/(?P<name>[A-Za-z_\-]+)/(?P<genre_id>\d+)/$', 'src.seeker.views.genre'),
        (r'^preferences/$', 'src.seeker.views.preferences'),
        (r'^search-post/$', 'src.seeker.views.search_post'),
        (r'^search/json/$', 'src.seeker.views.search_json'),
)
