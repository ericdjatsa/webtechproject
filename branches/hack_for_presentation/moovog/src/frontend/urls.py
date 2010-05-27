# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'src.frontend.views.index'),
    (r'^add_to_db/(?P<step>[1,2])/$', 'src.frontend.views.add_to_db'),
    (r'^movie/(?P<name>[A-Za-z_\-]+)/(?P<movie_id>\d+)/$', 'src.frontend.views.movie'),
    (r'^movie/(?P<name>[A-Za-z_\-]+)/(?P<movie_id>\d+)/watch$', 'src.frontend.views.movie_watch'),
    (r'^person/(?P<name>[A-Za-z_\-]+)/(?P<person_id>\d+)/$', 'src.frontend.views.person'),
    (r'^character/(?P<name>[A-Za-z_\-]+)/(?P<character_id>\d+)/$', 'src.frontend.views.character'),
    (r'^genre/(?P<name>[A-Za-z_\-]+)/(?P<genre_id>\d+)/$', 'src.frontend.views.genre'),
    (r'^preferences/$', 'src.frontend.views.preferences'),
    (r'^search/$', 'src.frontend.views.search_post'),
    (r'^search/(?P<search_type>(movie)|(person)|(character)|(genre))/(?P<search_query>[A-Za-z0-9+_\-]*)/$', 'src.frontend.views.search'),
)
