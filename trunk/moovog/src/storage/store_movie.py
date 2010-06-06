# -*- coding: utf-8 -*-
from src.seeker.workflows import * 
from src.seeker.models import *
import threading
from threading import Thread, Lock
from convert_date import *
from parse_aka import *
import imdb
from datetime import date
import time
from django.utils.encoding import smart_str, smart_unicode

# /////////////thread classes for storing ///////

def thread_still_alive(list_of_threads):
    for thread in list_of_threads:
        if thread is not None:
            if thread.is_alive(): return True
    return False

def search_movie_for_moovog(files, max_results):
    dict = {}
    threads = {}
    if files is not ([] or None):
        for file in files:
            while threading.active_count() > Thread_store_movie.MAX_THREAD_QUOTA: time.sleep(1.0)
            thread = Thread_search_movie(file.filename, max_results)
            threads[file.id] = thread
            print "searching movie : %s (%s)" % (str(thread.filename), str(thread.name))
            thread.start()
        while thread_still_alive(threads.values()): time.sleep(1.0)
#        time.sleep(10)
        for key in threads.iterkeys():
            dict[key] = threads[key].result_list
#            print (str(threads[key].name) + " : " + str(dict[key]))
    return dict

class Thread_search_movie(threading.Thread):
    """
        INPUT :
            filename
            max_results
        OUTPUT
            list of imdb objects
    """
    def __init__(self, filename, max_results):
        threading.Thread.__init__(self)
        self.filename = filename
        self.max_results = max_results
        self.result_list = []
        
    
    def run(self):
        i = imdb.IMDb()
        self.result_list = i.search_movie(self.filename)[:self.max_results]
        print "received %s responses (%s)" % (str(len(self.result_list)), str(self.name))
#        for result in result_list:
#            print "updating : %s" % str(result)
#            i.update(result)
        print "search DONE for search objective : %s (%s)" % (str(self.filename), str(self.name))
        self._Thread__stop()
        return True

class Thread_store_actor_and_character(threading.Thread):
    """
        INPUT :
            actor
            movie
        OUTPUT :
            actor-model
    """
    def __init__(self, person, movie):
        threading.Thread.__init__(self)
        self.person = person
        self.movie = movie
        self.actor = None
        self.character = None
        
    def run(self):
        i = imdb.IMDb()
        i.update(self.person)
        
        Input = {}
        Input['imdb-id'] = self.person.getID()
        Input['full-name'] = self.person['name']

        try: Input['thumbnail-url'] = self.person["headshot"]
        except Exception, x: Input['thumbnail-url'] = None
        try: Input['nick-name'] = self.person["akas"][0]
        except Exception, x: Input['nick-name'] = None
        try: Input['birth-date']= str(self.person.get('birth date'))
        except Exception, x: Input['birth-date'] = None
        try: Input['place-of-birth'] = self.person["birth notes"]
        except Exception, x: Input['place-of-birth'] = None
        try: Input['death-date'] = str(self.person.get('death date'))
        except Exception, x: Input['death-date'] = None
        try: Input['place-of-death'] = self.person["death notes"]
        except Exception, x: Input['place-of-death'] = None
        try: Input['mini-story'] = str(self.person['mini biography'])
        except Exception, x: Input['mini-story'] = None
        
        # Storing the actor in seeker's models
        actor_creation = Create_Or_Get_Actor_WF(Input, None)
        with threading.Lock() as lock: actor_creation.work()
        self.actor = actor_creation.response()['actor-model']

        def record_character(self, a):
            self.character = Character_Model.get_character_model_by_imdb_id(self.person.currentRole.getID())
            if self.character is None:
                print "storing character : %s (current thread : %s)" % (str(self.person.currentRole), str(self.name))
                input_character = {}
                input_character['imdb-id'] = self.person.currentRole.getID()
                input_character['character-name'] = str(self.person.currentRole)
                input_character['related-actor'] = self.actor
                input_character['related-movie'] = self.movie
                
                # Storing the role of the actor in seeker's models
                character_creation = Create_Or_Get_Character_WF(input_character, None)
                with threading.Lock() as lock: character_creation.work()
                self.character = character_creation.response()["character-model"]

        try:
            self.person.currentRole.getID()
            record_character(self, self.actor)
        except Exception, x:
            print "no imdb id for character '%s' : operation abortion (current thread : %s)" % (str(self.person.currentRole), str(self.name))

        self._Thread__stop()

class Thread_store_director(threading.Thread):
    """
        INPUT :
            director
            movie
        OUTPUT :
            director-model
    """
    def __init__(self, person, movie):
        threading.Thread.__init__(self)
        self.person = person
        self.movie = movie
        self.director = None
        
    def run(self):
        i = imdb.IMDb()
        i.update(self.person)
        
        Input = {}
        Input['imdb-id'] = self.person.getID()
        Input['full-name'] = self.person['name']

        try: Input['thumbnail-url'] = self.person["headshot"]
        except Exception, x: Input['thumbnail-url'] = None
        try: Input['nick-name'] = self.person["akas"][0]
        except Exception, x: Input['nick-name'] = None
        try: Input['birth-date']= str(self.person.get('birth date'))
        except Exception, x: Input['birth-date'] = None
        try: Input['place-of-birth'] = self.person["birth notes"]
        except Exception, x: Input['place-of-birth'] = None
        try: Input['death-date'] = str(self.person.get('death date'))
        except Exception, x: Input['death-date'] = None
        try: Input['place-of-death'] = self.person["death notes"]
        except Exception, x: Input['place-of-death'] = None
        try: Input['mini-story'] = str(self.person['mini biography'])
        except Exception, x: Input['mini-story'] = None
        
        # Storing the director in seeker's models
        director_creation = Create_Or_Get_Director_WF(Input, None)
        with threading.Lock() as lock: director_creation.work()
        self.director = director_creation.response()['director-model']
        self._Thread__stop()

class Thread_store_writer(threading.Thread):
    """
        INPUT :
            writer
            movie
        OUTPUT :
            writer-model
    """
    def __init__(self, person, movie):
        threading.Thread.__init__(self)
        self.person = person
        self.movie = movie
        self.writer = None
        
    def run(self):
        i = imdb.IMDb()
        i.update(self.person)
        
        Input = {}
        Input['imdb-id'] = self.person.getID()
        Input['full-name'] = self.person['name']

        try: Input['thumbnail-url'] = self.person["headshot"]
        except Exception, x: Input['thumbnail-url'] = None
        try: Input['nick-name'] = self.person["akas"][0]
        except Exception, x: Input['nick-name'] = None
        try: Input['birth-date']= str(self.person.get('birth date'))
        except Exception, x: Input['birth-date'] = None
        try: Input['place-of-birth'] = self.person["birth notes"]
        except Exception, x: Input['place-of-birth'] = None
        try: Input['death-date'] = str(self.person.get('death date'))
        except Exception, x: Input['death-date'] = None
        try: Input['place-of-death'] = self.person["death notes"]
        except Exception, x: Input['place-of-death'] = None
        try: Input['mini-story'] = str(self.person['mini biography'])
        except Exception, x: Input['mini-story'] = None
        
        # Storing the director in seeker's models
        writer_creation = Create_Or_Get_Writer_WF(Input, None)
        with threading.Lock() as lock: writer_creation.work()
        self.writer = writer_creation.response()['writer-model']
        self._Thread__stop()

class Thread_award_section(threading.Thread):
    """
        INPUT :
            movie (a Movie_Model)
            award (an Award_Model)
            category (a Award_Category_Model)
            person (Actor_Model/Writer_Model/Director_Model)
        OUTPUT :
            (empty)
    """
    
    def __init__(self, person, person_category, film, award, category):
        threading.Thread.__init__(self)
        self.person = person
        self.person_category = person_category
        self.award = award
        self.category = category
        self.film = film
        self.match = None
        
    def run(self):
        input_matcher = {}
        input_matcher['movie-model'] = self.film
        input_matcher['award-model'] = self.award
        input_matcher['award-category-model'] = self.category
        input_matcher['actor-model'] = None
        input_matcher['director-model'] = None
        input_matcher['writer-model'] = None
        
        if self.person_category == "actor":
            input_matcher['actor-model'] = Actor_Model.get_actor_model_by_imdb_id(self.person.getID())            
        elif self.person_category == "director":
            input_matcher['director-model'] =  Director_Model.get_director_model_by_imdb_id(self.person.getID())
        elif self.person_category == "writer":
            input_matcher['writer-model'] =  Writer_Model.get_writer_model_by_imdb_id(self.person.getID())
        
        matcher_creation = Create_Or_Get_Award_Matcher_WF(input_matcher, None)
        with threading.Lock() as lock: matcher_creation.work()
        self.match = matcher_creation.response()["award-matcher-model"]
        self._Thread__stop()

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

class Thread_store_movie(threading.Thread):
#    """
#        INPUT :
#            Store_movie object
#        OUTPUT :
#            (empty)
#    """
#    
#    def __init__(self, s_m_o):
#        threading.Thread.__init__(self)
#        self.store_movie_object = s_m_o
#        
#    def run(self):
#        s_m_o.start()
#        self._Thread__stop()
#
#class Store_movie():
    MAX_THREAD_QUOTA = 20 # reduce the risk of dead lock or cpu bottlenecks

    def __init__(self, movie, fichier):
        threading.Thread.__init__(self)
        self.movie = movie
        self.fichier = fichier

    def run(self):
        start = time.time()
        
        #Starting the movie
        print ""
        print 'starting movie %s...' % smart_str(self.movie["title"])
        
        def upgrade_movie(movie):
            i = imdb.IMDb()
            i.update(movie)
            return movie
        
        print "seeking information for movie on imdb..."
        next_step = False
        while next_step is False:
            try:
                self.movie = upgrade_movie(self.movie)
                next_step = True
            except Exception, x:
                print x
                next_step = False
        
        start_movie = {}
        start_movie['imdb-id'] = self.movie.getID()
        start_movie['original-title'] = smart_str(self.movie['title'])
        start_movie['filename'] = self.fichier.filename
        start_movie['extension'] = self.fichier.extension
        start_movie['path-on-disk'] = self.fichier.path
        start_movie['hashcode'] = self.fichier.hash_code

        movie_creation = Create_Or_Get_Movie_WF(start_movie, None).work()
        film = movie_creation['movie-model']
        print 'movie started...'

        #///Storing actors ////////
        print 'storing actors...'
        actor_threads = []
        acteurs = []
        try:
            actors = self.movie['actors']
        except Exception, x:
            actors = []
            print "problem with self.movie['actors']"
        for actor in actors:
            while threading.active_count() > Thread_store_movie.MAX_THREAD_QUOTA: time.sleep(1.0)
            a = Actor_Model.get_actor_model_by_imdb_id(actor.getID())
            if a is None:
                print "storing actor : %s" % smart_str(actor)
                thread = Thread_store_actor_and_character(actor, film)
                actor_threads.append(thread)
                thread.start()
            else: acteurs.append(a)

        #////storing directors/////
        print 'storing directors...'
        director_threads = []
        directeurs = []
        try:
            directors = self.movie['director']
        except Exception, x:
            directors = []
            print "problem with self.movie['director']"
        for director in directors:
            while threading.active_count() > Thread_store_movie.MAX_THREAD_QUOTA: time.sleep(1.0)
            d = Director_Model.get_director_model_by_imdb_id(director.getID())
            if d is None:
                print "storing director : %s" % smart_str(director)
                thread = Thread_store_director(director, film)
                director_threads.append(thread)
                thread.start()
            else: directeurs.append(d)

        #///////storing writers//////////
        print 'storing writers...'
        writer_threads = []
        ecrivains = []
        try:
            writers = self.movie['writer']
        except Exception, x:
            writers = []
            print "problem with self.movie['writer']"
        for writer in writers:
            while threading.active_count() > Thread_store_movie.MAX_THREAD_QUOTA: time.sleep(1.0)
            w = Writer_Model.get_writer_model_by_imdb_id(writer.getID())
            if w is None:
                print "storing writers : %s" % smart_str(writer)
                thread = Thread_store_writer(writer, film)
                writer_threads.append(thread)
                thread.start()
            else: ecrivains.append(w)
        
        while threading.active_count() > 10:
            time.sleep(1.0)
            print "waiting... still " +str(threading.active_count()) + " processes running (step 1/2)..."
            
        for a_t in actor_threads:
            if a_t is not None:
                acteurs.append(a_t.actor)
        for d_t in director_threads:
            if d_t is not None:
                directeurs.append(d_t.director)
        for w_t in writer_threads:
            if w_t is not None:
                ecrivains.append(w_t.writer)
        print "all actors, directors, writers have been processed"

#        //////////storing countries//////////
        pays = []
        try:
            countries = self.movie['country']
        except Exception, x:
            countries = []
            print "problem with self.movie['country']"
        for country in countries:
            country_input = {'country-name' : smart_str(country)}
            country_creation = Create_Or_Get_Country_WF(country_input, None).work()
            c = country_creation['country-model']
            pays.append(c)
        print 'all countries stored'

        #/////////storing genres//////////
        genres = []
        try:
            kinds = self.movie['genre']
        except Exception, x:
            kinds = []
            print "problem with self.movie['genre']"
        for kind in kinds:
            genre_input = {'genre-name' : smart_str(kind)}
            genre_creation = Create_Or_Get_Genre_WF(genre_input, None).work()
            g = genre_creation['genre-model']
            genres.append(g)
        print 'all genres stored'

        #/////////////storing akas////////////////
        try:
            akas = self.movie['aka']
        except Exception, x:
            akas = []
            print "problem with self.movie['akas']"
        k = 0 
        for aka in akas:
            try:
                countries = []
                aka_name = parse_aka(smart_str(aka))['aka']
                for c in parse_aka(smart_str(aka))['countries']:
                    p = Create_Or_Get_Country_WF({'country-name' : c}, None).work()['country-model']
                    countries.append(p)
                aka_input = {}
                aka_input['aka-name'] = aka_name
                aka_input['movie-model'] = film
                aka_input['country-models'] = countries
                A = Create_Or_Get_Aka_WF(aka_input, None).work()
            except Exception, x:
                print x
                pass
        print 'all akas stored'

        #/////////store release date///////////////////
        try:
            year = self.movie['year']
        except Exception, x:
            year = None
            print "problem with self.movie['year']"
            
        input_release_date = {}
        input_release_date['release-date'] = date(year, 1, 1)
        input_release_date['movie-model'] = film
        input_release_date['country-models'] = pays
        release_creation = Create_Or_Get_Release_Date_WF(input_release_date, None)
        release_creation.work()
        print 'release date stored'
    
        #////////complete Movie///////
        input_complete_movie = {}
        try: input_complete_movie['runtime'] = str(self.movie['runtime'][0])
        except: input_complete_movie['runtime'] = None
        try: input_complete_movie['user-rating'] = self.movie['user rating']
        except: input_complete_movie['user-rating'] = None
        try: input_complete_movie['thumbnail-url'] = str(self.movie['cover'])
        except: input_complete_movie['thumbnail-url'] = None
        input_complete_movie['movie-model'] = film
        input_complete_movie['original-countries'] = pays
        try: input_complete_movie['actors'] = acteurs
        except: input_complete_movie['actors'] = None
        try: input_complete_movie['writers'] = ecrivains
        except: input_complete_movie['writers'] = None
        try: input_complete_movie['directors'] = directeurs
        except: input_complete_movie['directors'] = None
        input_complete_movie['genres'] = genres
        try: input_complete_movie['plot'] = self.movie['plot'][1]
        except: input_complete_movie['plot'] = "no plot available"
        try: input_complete_movie['summary'] = self.movie['plot'][0]
        except: input_complete_movie['summary'] = "no summary available"
        complete_movie = Complete_Movie_Model_WF(input_complete_movie, None)
        complete_movie.work()
        print 'movie completed...'

        def upgrade_movie_with_awards(movie):
            i = imdb.IMDb()
            i.update(movie, info = ['awards'])
            return movie
        
        print "creating matches between persons, movies, awards and award categories..."
        next_step = False
        while next_step is False:
            try:
                movie_upgraded = upgrade_movie_with_awards(self.movie)
                next_step = True
            except Exception, x:
                print x
                next_step = False
        
        if movie_upgraded.has_key("awards"):
            for award in movie_upgraded['awards']:
                input_award = {}
                input_award['award-name'] = smart_str(award['award'])
                input_award['date-of-awarding'] = date(award['year'], 1, 1)
                input_award['award-status'] = smart_str(award['result'])
                award_creation = Create_Or_Get_Award_WF(input_award, None).work()
                award_model = award_creation['award-model']

                if award.has_key("category"):
                    input_award_category = {}
                    input_award_category['award-category-name'] = smart_str(award['category'])
                    category_creation = Create_Or_Get_Award_Category_WF(input_award_category, None).work()
                    category = category_creation['award-category-model']
                else: category = None
    
                for person in award['to']:
                    while threading.active_count() > Thread_store_movie.MAX_THREAD_QUOTA: time.sleep(1.0)
                    
                    print "award matching for :"
                    print "    award : %s" % smart_str(award_model.award_name)
                    if category is None: print "    category : no category found"
                    else: print "    category : %s" % category.__unicode__()
                    print "    person : %s" % smart_str(person)
                    
                    if person in actors:
                        Thread_award_section(person, "actor", film, award_model, category).start()
                    elif person in directors:
                        Thread_award_section(person, "director", film, award_model, category).start()
                    elif person in writers:
                        Thread_award_section(person, "writer", film, award_model, category).start()
                    else: Thread_award_section(person, "unknown", film, award_model, category).start()
                    
            while threading.active_count() > 10:
                time.sleep(1.0)
                print "waiting... still " +str(threading.active_count()) + " processes running (step 2/2)..."
            
            print 'all awards stored'
        
        self._Thread__stop()
        print "storage DONE."
        print "operation took : %s seconds" % str(time.time() - start)