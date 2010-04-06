
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^sandbox/$', 'playground.sandbox.views.index'),
#    (r'^polls/(?P<poll_id>\d+)/$', 'mysite.polls.views.detail'),
#    (r'^polls/(?P<poll_id>\d+)/results/$', 'mysite.polls.views.results'),
#    (r'^polls/(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),
)
