# -*- coding: utf-8 -*-
from moovog.src.seeker.workflows import * 
from moovog.src.seeker.models import *
import threading
from convert_date import *
from parse_aka import *
from moovog import imdb



# /////////////thread classes for storing ///////


#Actors + carachter
class Thread_store_actor(threading.Thread):
    def __init__(self,person,movie,table,table_done):
        threading.Thread.__init__(self)
        self.table_done=table_done
        self.order=len(table_done)
        self.table_done.append(0) 
        self.person = person
        self.movie=movie
        self.table = table
    def run(self):
        #print '===========store started========='  
        a = Actor_Model.get_actor_model_by_imdb_id(self.person.getID())
        if (a == None):

            #///IMDB Instance////
            i = imdb.IMDb()
            i.update(self.person)
            #///////////////////

            #///////stroing actor in database////////
            Input={}
            Input['imdb-id']= self.person.getID()
            Input['full-name']= self.person['name']
            Input['nick-name']=None
            Input['thumbnail-url']=None

            try:
                Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            except:
                Input['birth-date']=None
            
            try:
                Input['mini-story']= self.person['biography']
            except:
                Input['mini-story']= None
            try: 
                Input['death-date']= convert_date(self.person.get('death date'))
            except:
                Input['death-date']=None
         

            try:
                actor_creation = Create_Or_Get_Actor_WF(Input,None)
                a=actor_creation.process()
                a = actor_creation.response()['actor-model']
            except: pass
         #       print 'cannot store actor' 


            Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            Input['mini-story']= self.person['biography']
            Input['death-date']= convert_date(self.person.get('death date'))
            Input['thumbnail-url']= None
            Input['nick-name']= None
		#		Input['thumbnail-url']= None
            actor_creation = Create_Or_Get_Actor_WF(Input,None)
            actor_creation.process()
            a = actor_creation.response()['actor-model']

            #///////////////////////////////////////////
        if (a!=None):
            self.table.append(a) 
        
        #////Storing the Role of the actor/////
            try:
                Input={}
                Input['imdb-id']=self.person.currentRole.getID()
                Input['character-name']=self.person.currentRole.__str__()
                Input['related-actor']=a
                Input['related-movie']=self.movie
                character_creation = Create_Or_Get_Character_WF(Input,None) 
                character_creation.process()
            except:pass
          #      print 'cannot store role' 

        #///////////////////////////////////////////
        

        self.table_done[self.order]=1
        #print '==========store Actor and role done==============='
        self._Thread__stop()

#Directors
class Thread_store_director(threading.Thread):
    def __init__(self,person,table,table_done):
        threading.Thread.__init__(self)
        self.table_done=table_done
        self.order=len(table_done)
        self.table_done.append(0) 
        self.person = person
        self.table = table 
    def run(self):
        #print '===========store started========='  
        a = Director_Model.get_director_model_by_imdb_id(self.person.getID())
        if (a == None):
            i = imdb.IMDb()
            i.update(self.person)
            #print 'nick name'+actor['nicks']

            Input={}
            Input['imdb-id']= self.person.getID()
            Input['full-name']= self.person['name']
            Input['thumbnail-url']=None
            Input['nick-name']=None
            try:
                Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            except:
                Input['birth-date']=None
            
            try:
                Input['mini-story']= self.person['biography']
            except:
                Input['mini-story']= None
            try: 
                Input['death-date']= convert_date(self.person.get('death date'))
            except:
                Input['death-date']=None
            
            try:
                director_creation = Create_Or_Get_Director_WF(Input,None)
                adirector_creation.process()
                a = director_creation.response()['director-model']
            except:
                pass
        if (a!=None):
            self.table.append(a) 
        
        

            Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            Input['mini-story']= self.person['biography']
            Input['death-date']= convert_date(self.person.get('death date'))
            Input['thumbnail-url']= None
            Input['nick-name']= None
            director_creation = Create_Or_Get_Director_WF(Input,None)
            director_creation.process()
            a = director_creation.response()['director-model']
        self.table.append(a) 

        self.table_done[self.order]=1
        #print '==========unpdate done==============='
        self._Thread__stop()
#Writers
class Thread_store_writer(threading.Thread):
    def __init__(self,person,table,table_done):
        threading.Thread.__init__(self)
        self.table_done=table_done
        self.order=len(table_done)
        self.table_done.append(0) 
        self.person = person
        self.table = table 
    def run(self):
        #print '===========store started========='  
        a = Writer_Model.get_writer_model_by_imdb_id(self.person.getID())
        if (a == None):
            i = imdb.IMDb()
            i.update(self.person)
            #print 'nick name'+actor['nicks']
            Input={}
            Input['imdb-id']= self.person.getID()
            Input['full-name']= self.person['name']
            Input['nick-name']=None
            Input['thumbnail-url']=None
            try:
                Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            except:
                Input['birth-date']=None
            
            try:
                Input['mini-story']= self.person['biography']
            except:
                Input['mini-story']= None
            try: 
                Input['death-date']= convert_date(self.person.get('death date'))
            except:
                Input['death-date']=None

            try:
                writer_creation = Create_Or_Get_Writer_WF(Input,None)
                a=writer_creation.process()
                a = writer_creation.response()['writer-model']
            except:
                pass
        if (a!=None):  
            self.table.append(a)


            Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            Input['mini-story']= self.person['biography']
            Input['death-date']= convert_date(self.person.get('death date'))
            Input['thumbnail-url']= None
            Input['nick-name']= None
            writer_creation = Create_Or_Get_Writer_WF(Input,None)
            writer_creation.process()
            a = writer_creation.response()['writer-model']
        self.table.append(a) 
        self.table_done[self.order]=1
        #print '==========unpdate done===============
        self._Thread__stop()

#///Awards macher thread///

def person_is(person,movie):

    table=[]
    for writer in movie['writer']:
        if (writer.getID() == person.getID()): table.append('writer')
        else: pass

    for actor in movie['actors']:
        if (actor.getID() == person.getID()): table.append('actor')
        else: pass

    for director in movie['director']:
        if (writer.getID() == person.getID()): table.append('director')
        else: pass

    return table



class Thread_award_matcher(threading.Thread):
    def __init__(self,person,film,movie,award,category,table_done):
        threading.Thread.__init__(self)
        self.table_done=table_done
        self.order=len(table_done)
        self.table_done.append(0) 
        self.person = person
        self.award = award
        self.category = category
        self.film = film
        self.movie = movie
        
    def run(self):
        #print '/////award matching started/////////'
        if ('actor' in person_is(self.person,self.movie)):
            Input={}
            Input['movie-model']=self.film
            Input['award-model']=self.award
            Input['award-category-model']=self.category
            actor = Actor_Model.get_actor_model_by_imdb_id(self.person.getID())
            Input['actor-model']= actor
            Input['director-model']= None            Input['writer-model']= None
            matcher_creation=Create_Or_Get_Award_Matcher_WF(Input,None)
            matcher_creation.process()
            #print 'award found for an actor'

        if ('director' in person_is(self.person,self.movie)):
            Input={}
            Input['movie-model']=self.film
            Input['award-model']=self.award
            Input['award-category-model']=self.category
            director = Director_Model.get_director_model_by_imdb_id(self.person.getID())
            Input['actor-model']= None
            Input['director-model']= director            Input['writer-model']= None
            matcher_creation=Create_Or_Get_Award_Matcher_WF(Input,None)
            matcher_creation.process()
            #print 'award found for director'

        if ('writer' in person_is(self.person,self.movie)):
            Input={}
            Input['movie-model']=self.film
            Input['award-model']=self.award
            Input['award-category-model']=self.category
            writer = Writer_Model.get_writer_model_by_imdb_id(self.person.getID())
            Input['actor-model']= None
            Input['director-model']= None            Input['writer-model']= writer
            matcher_creation=Create_Or_Get_Award_Matcher_WF(Input,None)
            matcher_creation.process()
            #print 'award found for writer'
 
        else:
            Input={}
            Input['movie-model']=self.film
            Input['award-model']=self.award
            Input['award-category-model']=self.category
            Input['actor-model']= None
            Input['director-model']= None            Input['writer-model']= None
            matcher_creation=Create_Or_Get_Award_Matcher_WF(Input,None)
            matcher_creation.process()
            #print 'award found for no one :D'
        #print '/////////award matchinf finnished/////////'
        self.table_done[self.order]=1
        self._Thread__stop()
       



#/////////////////////////////////////////////////////
    

class Store_movie():

    def __init__(self,movie,fichier):
        self.movie = movie
        self.fichier = fichier


    def start(self):

        #Storing te movie
        print 'storing movie...'
        Input={}
        Input['imdb-id']=self.movie.getID()
        Input['original-title']= self.movie['title'].__str__()
        Input['filename']= self.fichier.filename
        Input['extension']= self.fichier.extension
        Input['path-on-disk']= self.fichier.path
        Input['hashcode']=self.fichier

        movie_creation = Create_Or_Get_Movie_WF(Input,None)
        movie_creation.process()
        film = movie_creation.response()['movie-model']

        print 'movie stored'
        
        #///Storing Actors ////////
        table_done=[]
        print 'storing actors...' 
        acteurs = []
        actors = self.movie['actors']
        for actor in actors:
            Thread_store_actor(actor,film,acteurs,table_done).start()
        
        done = 0
        while(done == 0):
            done=1
            for j in table_done:
                done = done * j
        print 'actors stored'
        

        #////storing Directors/////
        print 'storing directors...'
        table_done=[]
        directeurs = []
        directors = self.movie['director']
        for director in directors:
            Thread_store_director(director,directeurs,table_done).start()

        done = 0
        while(done == 0):
            done=1
            for j in table_done:
                done = done * j
        print 'directors stored'


        #///////storing wiriters//////////
        print 'storing writers...'
        table_done=[]
        ecrivains = []
        writers = self.movie['writer']
        for writer in writers:
            Thread_store_writer(writer,ecrivains,table_done).start()

        done = 0
        while(done == 0):
            done=1
            for j in table_done:
                done = done * j
        print 'writers stored'

        


        #//////////stroing countries//////////

        pays = []
        countries = self.movie['country']
        for country in countries:
            Input = {'country-name':country.__str__()}
            country_creation = Create_Or_Get_Country_WF(Input,None)
            country_creation.process()
            c = country_creation.response()['country-model']
            pays.append(c)
        print 'countries stored' 

        #/////////storing genres//////////
        genres = []
        kinds = self.movie['genre']
        for kind in kinds:
            Input = {'genre-name':kind.__str__()}
            genre_creation = Create_Or_Get_Genre_WF(Input,None)
            genre_creation.process()
            g = genre_creation.response()['genre-model']
            genres.append(g)

        print 'genres stored' 


        #//////////Store Synopsis/////////
        #Input={}
        #Input['plain-text']=self.movie['plot']
        #Input['movie-model']=film
        #Input['country-models']=pays
        #synopsis_creation=Create_Or_Get_Synopsis_WF(Input,None)
        #synopsis_creation.process()
        Input={}
        Input['plain-text']=self.movie['plot']
        Input['movie-model']=film
        Input['country-models']=pays
        synopsis_creation=Create_Or_Get_Synopsis_WF(Input,None)
        synopsis_creation.process()

        #/////////////storing aka////////////////
        akas = self.movie['aka']
        k=0 
        for aka in akas:
            try:
                couuntries=[]
                aka_name = parse_aka(aka.__str__())['aka']
            
                for c in parse_aka(aka.__str__())['countries']:
                    p =  Create_Or_Get_Country_WF({'country-name':c},None).work()['country-model']
                    couuntries.append(p)
                Input={}
                Input['aka-name']=aka_name
                Input['movie-model']=film
                Input['country-models']=couuntries
                A=Create_Or_Get_Aka_WF(Input,None).work()
            except:
                pass   
                #print 'cannot add aka'
        print 'akas stored' 


        #/////////store release date///////////////////
        Input={}
        Input['release-date']=str(self.movie['year'])+'-'+'01'+'-'+'01'
        Input['movie-model']=film
        Input['country-models']=pays       
        release_creation=Create_Or_Get_Release_Date_WF(Input,None)
        release_creation.process()
        print 'release date stored' 



    
        #////////complete Movie///////
        Input = {}
        Input['runtime']=self.movie['runtime'][0].__str__()
        Input['user-rating']=self.movie['user rating']
        Input['thumbnail-url']=self.movie['cover'].__str__()
        Input['movie-model']=film
        Input['original-countries']=pays
        Input['actors']=acteurs
        Input['writers']=ecrivains
        Input['directors']=directeurs
        Input['genres']=genres
        Input['plot']=self.movie['plot'][1]
        Input['summary']=self.movie['plot'][0]

        complete_movie = Complete_Movie_Model_WF(Input,None)
        complete_movie.process()

        print 'movie completed' 

         #stroing Awards for the movie
        i=imdb.IMDb()
        i.update(self.movie,info=['awards'])
        #awards+categories
        awards = []
        table_done=[]
        for award in self.movie['awards']:
            try:
                #award
                Input= {}
                Input['award-name']=award['award'].__str__()
                Input['date-of-awarding']=str(award['year'])+'-'+'01'+'-'+'01'
                Input['award-status']=award['result'].__str__()
                award_creation=Create_Or_Get_Award_WF(Input,None)
                award_creation.process()
                awward=award_creation.response()['award-model']
                #if (award_creation.response()['already-existed']==True): print  award['award'].__str__() +' award already exists'

            except:
                #print 'award cannot be stored'
                pass
            #category
            try:
                Input={}
                Input['award-category-name']=award['category'].__str__()
                category_creation=Create_Or_Get_Award_Category_WF(Input,None)
                category_creation.process()
                category=category_creation.response()['award-category-model']
            except:
                pass

            #matching
       
            for person in award['to']:
                #try:
                    caategory=category
                    Thread_award_matcher(person,film,self.movie,awward,caategory,table_done).start()
                #except: pass

 
        done = 0 
        while(done == 0):
            done=1
            for j in table_done:
                done = done * j

        print 'awards stored' 


        print '//////////////////////////////////////////////////////////////////////////////'
        print '////////////////////////////////STORAGE DONE ;-)//////////////////////////////////'
        print '//////////////////////////////////////////////////////////////////////////////'

                   
                #category
                #Input={}
         #       Input['award-category-name']=award['category'].__str__()
          #      category_creation = Create_Or_Get_Award_Category_WF(Input,None)
           #     category =category_creation.work()['award-category-model']
            #    categories.append(category)
            #except:
             #   pass
         
        #award
        #awards = []
          

        #matcher         


        
              
