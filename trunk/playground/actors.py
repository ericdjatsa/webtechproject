#!/usr/bin/env python

from django.core.management import setup_environ
import settings
from ranker.models import *
from operator import attrgetter
import sys

setup_environ(settings)

a = Actor_Model()
a.full_name='Morgan Freeman Georges'
a.nick_name='the veteran'
print 'created Actor_model : a, with full_name= "Morgan Freeman Georges" and nick_name="the veteran" '

b=Actor_Model()
b.full_name='Samuel Lee Clooney Jackson'
b.nick_name='the professional'
print 'created Actor_model : b, with full_name= "Samuel Lee Clooney Jackson" and nick_name= "the professional" '

c=Actor_Model()
c.full_name='Georges Clooney Morgan'
c.nick_name='handsome man'
print 'created Actor_model : c, with full_name= "Georges Clooney Morgan" and nick_name= "handsome man" '

d=Actor_Model()
d.full_name='Nicole Samuel Kidman Freeman'
d.nick_name='blond lady'
print 'created Actor_model : d, with full_name= "Nicole Samuel Kidman Freeman" and nick_name="blond lady" '


search_string=sys.argv[1]
print 'Ranking: search_string: ',search_string

a.rank(search_string)
b.rank(search_string)
c.rank(search_string)
d.rank(search_string)
actors=[a,b,c,d]
#two methods for sorting
#sorted(student_tuples, key=lambda student: student[2])
#sorted(student_objects, key=attrgetter('age'), reverse=True)
ranked_actors=sorted(actors,key=attrgetter('rank_value'),reverse=True) #NB: attrgetter works for python 2.5 and newer
#the above line is equivalent to sorted(awards,key=lambda award:award.rank_value,reverse=True)

print "Ranked Actors\n",ranked_actors
print "Actors ranks",map(attrgetter('rank_value'),ranked_actors)

#PLEASE CHECK THE CASE IN WHICH YOU MAKE A RANK WITH SEARCH_STRING= "Freeman Kidman"
