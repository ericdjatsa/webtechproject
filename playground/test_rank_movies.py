# -*- coding: utf-8 -*-
from django.core.management import setup_environ
import settings
from seeker.models import *
from seeker.repository import *
import sys

setup_environ(settings)




a = Test_Movie_Model(original_title='Avatar')
#a.original_title='Avatar'

akas_dict={}
akas_dict["akas_International"]='the amazing 3D film'
akas_dict["akas_France"]="Conquete d\'un nouveau monde"
a.set_info_akas(akas_dict)
a.user_rating=0.8

a.actors=['morgan','angelina']

print 'a.infos["akas"] ',a.infos["akas"]
print 'created Actor_model : a, with original_title= ',a.original_title,' and with akas  ',a.infos["akas"]

b=Test_Movie_Model()
b.original_title='Le fabuleux destin du petit Nicolas'
akas_dict={}
akas_dict["akas_International"]='the little Nico'
akas_dict["akas_France"]="Le brave garcon"
b.set_info_akas(akas_dict)
b.user_rating=0.7
b.actors=['brad','georges']
print 'created Actor_model : b, with original_title= ',b.original_title,' and with akas  ',b.infos["akas"]

c=Test_Movie_Model()
c.original_title='No country for old men'
akas_dict=dict()
akas_dict["akas_International"]='Get out of here'
akas_dict["akas_France"]="Allez Ouste"
c.set_info_akas(akas_dict)
c.user_rating=0.5
print 'c.infos["akas"] ',c.infos["akas"]

c.actors=['pierce','kidman']
print 'created Actor_model : c, with original_title= ',c.original_title,' and with akas  ',akas_dict

d=Test_Movie_Model()
d.original_title='Prince of Persia'
akas_dict=dict()
akas_dict["akas_International"]='The forgotten sands'
akas_dict["akas_France"]="Les sables oubliees" #NB problem with oubliées
d.set_info_akas(akas_dict)
d.user_rating=0.8
d.actors=['roger','moore']

e=Test_Movie_Model()
e.original_title='Iron Man'
akas_dict=dict()
akas_dict["akas_International"]='Metal justice'
akas_dict["akas_France"]="le justicier metalique" #NB problem with oubliées
e.set_info_akas(akas_dict)
e.user_rating=0.7

e.actors=['keanu','salma']
print 'created Actor_model : e, with original_title= ',e.original_title,' and with akas  ',akas_dict
akas_dict=dict()
actors=[a,b,c,d,e]

search_string=''
search_string=' '.join(str(w) for w in sys.argv[1:])
  
  
print 'Ranking: search_string: ',search_string

r=Repository()
rank_result=r.rank(a.kind(),actors,search_string)
print '\n\nrank results',rank_result
#print 'rank results',map(str,rank_result) # To display only the movie titles