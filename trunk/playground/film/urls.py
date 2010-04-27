
from django.conf.urls.defaults import *
from playground.film.models import Film

film_dict = {
	'queryset' : Film.objects.all(), 
	'paginate_by' : 24,
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', film_dict),
#    (r'^post/$', 'playground.film.views.post'),
    (r'^add_to_db/$', 'playground.film.views.add_to_db'),
#    (r'^message/(?P<msg_id>\d+)/$', 'playground.film.views.message'),
#    (r'^polls/(?P<poll_id>\d+)/$', 'mysite.polls.views.detail'),
#    (r'^polls/(?P<poll_id>\d+)/results/$', 'mysite.polls.views.results'),
#    (r'^polls/(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),
)
