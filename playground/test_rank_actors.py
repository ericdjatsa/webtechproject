# -*- coding: utf-8 -*-
from django.core.management import setup_environ
import settings
from seeker.models import *
from seeker.repository import *
from operator import attrgetter
import sys
import string

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

actors=[a,b,c,d]

search_string=''
search_string=' '.join(str(w) for w in sys.argv[1:])
  
  
print 'Ranking: search_string: ',search_string

r=Repository()
rnk=r.rank(a.kind(),actors,search_string)
print 'rank results',map(str,rnk)
