#!/usr/bin/env python

from django.core.management import setup_environ
import settings
from ranker.models import *
from operator import attrgetter

setup_environ(settings)

a = Award_Model()
a.award_name='Le fabuleux destin de Nicolas'
print 'created Award_model : a, with award_name= "Le fabuleux destin de Nicolas" '

b=Award_Model()
b.award_name='Le fabuleux'
print 'created Award_model : b, with award_name= "Le fabuleux" '

c=Award_Model()
c.award_name='Le destin de Nicolas'
print 'created Award_model : c, with award_name= "Le destin de Nicolas" '

d=Award_Model()
d.award_name='Le destin'
print 'created Award_model : d, with award_name= "Le destin" '

print 'Ranking: search_string: "destin Nicolas" '
search_string='destin Nicolas'

a.rank(search_string)
b.rank(search_string)
c.rank(search_string)
d.rank(search_string)
awards=[a,b,c,d]
#two methods for sorting
#sorted(student_tuples, key=lambda student: student[2])
#sorted(student_objects, key=attrgetter('age'), reverse=True)
ranked_awards=sorted(awards,key=attrgetter('rank_value'),reverse=True) #NB: attrgetter works for python 2.5 and newer
#the above line is equivalent to sorted(awards,key=lambda award:award.rank_value,reverse=True)

print "Ranked Awards\n",ranked_awards
print "Awards ranks",map(attrgetter('rank_value'),ranked_awards)
