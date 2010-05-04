
from django.conf.urls.defaults import *
from src.frontend.models import Film

film_dict = {
	'queryset' : Film.objects.all(), 
	'paginate_by' : 5,
}

film_detail_dict = {
	'queryset': Film.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', film_dict),
    (r'^add_to_db/$', 'src.frontend.views.add_to_db'),
    (r'^movie/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', film_detail_dict),
)
