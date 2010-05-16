from moovog.src.seeker.workflows import * 
from moovog.src.seeker.models import *
import imdb,threading
from convert_date import *



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
        print '===========store started========='  
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
            Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            Input['mini-story']= self.person['biography']
            Input['death-date']= convert_date(self.person.get('death date'))
            actor_creation = Create_Or_Get_Actor_WF(Input,None)
            actor_creation.process()
            a = actor_creation.response()['actor-model']
            #///////////////////////////////////////////
 
        self.table.append(a) 
        
        #////Storing the Role of the actor/////
        Input={}
        Input['imdb-id']=self.person.currentRole.getID()
        Input['character-name']=self.person.currentRole.__str__()
        Input['related-actor']=a
        Input['related-movie']=self.movie
        
        character_creation=Create_Or_Get_Character_WF(Input,None) 
        character_creation.process()
        #///////////////////////////////////////////
        

        self.table_done[self.order]=1
        print '==========store Actor and role done==============='
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
        print '===========store started========='  
        a = Director_Model.get_director_model_by_imdb_id(self.person.getID())
        if (a == None):
            i = imdb.IMDb()
            i.update(self.person)
            #print 'nick name'+actor['nicks']

            Input={}
            Input['imdb-id']= self.person.getID()
            Input['full-name']= self.person['name']
            Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            Input['mini-story']= self.person['biography']
            Input['death-date']= convert_date(self.person.get('death date'))
            director_creation = Create_Or_Get_Director_WF(Input,None)
            director_creation.process()
            a = director_creation.response()['director-model']
        self.table.append(a) 
        self.table_done[self.order]=1
        print '==========unpdate done==============='
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
        print '===========store started========='  
        a = Writer_Model.get_writer_model_by_imdb_id(self.person.getID())
        if (a == None):
            i = imdb.IMDb()
            i.update(self.person)
            #print 'nick name'+actor['nicks']
            Input={}
            Input['imdb-id']= self.person.getID()
            Input['full-name']= self.person['name']
            Input['birth-date']= convert_date(self.person.get('birth date').__str__())
            Input['mini-story']= self.person['biography']
            Input['death-date']= convert_date(self.person.get('death date'))
            writer_creation = Create_Or_Get_Writer_WF(Input,None)
            writer_creation.process()
            a = writer_creation.response()['writer-model']
        self.table.append(a) 
        self.table_done[self.order]=1
        print '==========unpdate done==============='
        self._Thread__stop()


#/////////////////////////////////////////////////////
    

class Store_movie():

    def __init__(self,movie,fichier):
        self.movie = movie
        self.fichier = fichier


    def start(self):
        Input = {'imdb-id':self.movie.getID(),'original-title':self.movie['title'].__str__() ,'filename':self.fichier.filename ,'extension':self.fichier.extension ,'path-on-disk':self.fichier.path ,'hashcode': self.fichier}
        movie_creation = Create_Or_Get_Movie_WF(Input,None)
        movie_creation.process()
        film = movie_creation.response()['movie-model']
        

        
        table_done=[]
        done=0
        #///Storing Actors ////////
        acteurs = []
        actors = self.movie['actors'][:4]
        for actor in actors:
            Thread_store_actor(actor,film,acteurs,table_done).start()


        #////storing Directors/////
        directeurs = []
        directors = self.movie['director']
        for director in directors:
            Thread_store_director(director,directeurs,table_done).start()

        #///////storing wiriters//////////
        ecrivains = []
        writers = self.movie['writer']
        for writer in writers:
            Thread_store_writer(writer,ecrivains,table_done).start()



        #//////////stroing countries//////////
        pays = []
        countries = self.movie['country']
        for country in countries:
            Input = {'country-name':country.__str__()}
            country_creation = Create_Or_Get_Country_WF(Input,None)
            country_creation.process()
            c = country_creation.response()['country-model']
            pays.append(c)

        #/////////storing genres//////////
        genres = []
        kinds = self.movie['genre']
        for kind in kinds:
            Input = {'genre-name':kind.__str__()}
            genre_creation = Create_Or_Get_Genre_WF(Input,None)
            genre_creation.process()
            g = genre_creation.response()['genre-model']
            genres.append(g)

        
        while(done == 0):
            done=1
            for j in table_done:
                done = done*j

        print '//////////////all threads have finnished/////////////'


        #//////////Store Synopsis/////////
        Input={}
        Input['plain-text']=self.movie['plot']
        Input['movie-model']=film
        Input['country-models']=pays
        synopsis_creation=Create_Or_Get_Synopsis_WF(Input,None)
        synopsis_creation.process()


        #/////////store release date///////////////////
        Input={}
        Input['release-date']=str(self.movie['year'])+'-'+'01'+'-'+'01'
        Input['movie-model']=film
        Input['country-models']=pays       
        release_creation=Create_Or_Get_Release_Date_WF(Input,None)
        release_creation.process()


    
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

        complete_movie = Complete_Movie_Model_WF(Input,None)
        complete_movie.process()
        
              
