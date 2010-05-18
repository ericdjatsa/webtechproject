# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from src.frontend.models import Film


film_detail_dict = {
	'queryset': Film.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'src.frontend.views.index'),
    (r'^add_to_db/(?P<step>[1,2])/$', 'src.frontend.views.add_to_db'),
    (r'^movie/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', film_detail_dict),
    (r'^preferences/$', 'src.frontend.views.preferences'),
)
