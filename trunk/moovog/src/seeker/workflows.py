'''
Created on 19 avr. 2010
@author: Christophe

This file gather all together the logic behind the views
'''

from base.Base_Workflow import Base_Workflow
from src.seeker.models import *
from tools.routines import homogeneous_search_dictionary_merger, heterogeneous_search_dictionary_merger

import logging
from datetime import datetime

class Search_WF(Base_Workflow):
    '''    
        This workflow only looks into the Movie_Model Table, and related ones
        
        INPUT :
            search-string
            search-option
        OUTPUT :
            search-result : a list of Movie_Model that correspond to the search
    '''
    
    SEARCH_OPTIONS = {u"unknown" : 'a', u"actor" : 'b', u"director" :'c', u"writer" : 'd',
                      u"movie-original-title" : 'e', u"movie-aka-title" : 'f', u"genre" : 'g',
                      u"character" : 'h', u"award" : 'i', u"award-category" : 'j', None : 'k'}
    
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("search-string")
        self.validate_string_field_not_empty("search-option")
    
    def process(self):
        start = datetime.now()
        search_string = self.request()["search-string"]
        strings_to_search = search_string.split()
        
        search_option = self.request()["search-option"]
        if search_option not in Search_WF.SEARCH_OPTIONS: search_option = None
        else:
            search_results = []
            for string_to_search in strings_to_search:
                search_result = {
                'a': lambda string_to_search: self.repository().search_all(string_to_search),
                'b': lambda string_to_search: self.repository().search_actor(string_to_search),
                'c': lambda string_to_search: self.repository().search_director(string_to_search),
                'd': lambda string_to_search: self.repository().search_writer(string_to_search),
                'e': lambda string_to_search: self.repository().search_movie(string_to_search),
                'f': lambda string_to_search: self.repository().search_aka(string_to_search),
                'g': lambda string_to_search: self.repository().search_genre(string_to_search),
                'h': lambda string_to_search: self.repository().search_character(string_to_search),
                'i': lambda string_to_search: self.repository().search_award(string_to_search),
                'j': lambda string_to_search: self.repository().search_award_category(string_to_search),
                'k': lambda string_to_search: None
                }[Search_WF.SEARCH_OPTIONS[search_option]](string_to_search)
                search_results.append(search_result)
            
        # TO DO : merge informations for different search_results
        # INPUT : search_results
        # Kill repetitions
        # Knock each elements from search_results against each others
        # OUTPUT : {"movie-models" : [movie_model, ...], actors-models : [actor_model, ...], ...}
        # (See search functions in seeker.repository.py to know all possible keys)
        merged_results = {}
        type_of_result = ""
        if search_option in [u"actor", u"director", u"writer", u"movie-original-title",
                             u"movie-aka-title", u"genre"]:
            type_of_result = "homogeneous"
            for dict in search_results:
                if dict is not None: merged_results = homogeneous_search_dictionary_merger(dict, merged_results)
        if search_option in [u"unknown", u"character", u"award", u"award-category"]:
            type_of_result = "heterogeneous"
            for dict in search_results:
                if dict is not None: merged_results = heterogeneous_search_dictionary_merger(dict, merged_results)
        
        # TO DO : page rank the result in merged_result (ERIC)
        # INPUT : merged_result
        # Sort them ascendantly
        # OUTPUT : page_ranked_result
        page_ranked_result = {}
        
        self.add_to_response("status", "ok")
        self.add_to_response("type-of-result", type_of_result)
        self.add_to_response("search-result", merged_results)
        self.add_to_response("time-to-serve", datetime.now() - start)
        
class Get_Infos_For_Homogeneous_Search_WF(Base_Workflow):
    """
        Converts models into string infos
        INPUT :
            dict-of-models : {key_model : [model_1; model_2, ...], ...}
        OUTPUT :
            result : {model_1 : [info_1, ...], ...}
            time-to-serve
    """
    def __init__(self, input, authorization_pipe):
        Base_Workflow.__init__(self, input, authorization_pipe)
        
    def validate_input(self):
        self.validate_list_field_not_empty("dict-of-models")
    
    def process(self):
        start = datetime.now()
        result = {}
        search_result = self.request()["dict-of-models"]
        for key in search_result.iterkeys():
            new_list = []
            for model in search_result[key]:
                new_list.append(model.get_infos_for_model())
            result[key] = new_list
                
        self.add_to_response("result", result)
        self.add_to_response("time-to-serve", datetime.now() - start)

class Get_Infos_For_Heterogeneous_Search_WF(Base_Workflow):
    """
        Converts models into string infos
        INPUT :
            dict-of-matches : {"match_1" : {key_model_1 : model_1, ...}, ...}
        OUTPUT :
            result : {"match_1" : {key_model_1 : [info_1, ...], ...}, ...}
            time-to-serve
    """
    def __init__(self, input, authorization_pipe):
        Base_Workflow.__init__(self, input, authorization_pipe)
        
    def validate_input(self):
        self.validate_("dict-of-matches")
    
    def process(self):
        start = datetime.now()
        result = {}
        search_result = self.request()["dict-of-matches"]
        i = 0
        
        for key in search_result.keys():
            for key_match in dict.keys():
                dict[key_match] = dict[key_match].get_infos_for_model()
            result[key] = dict
        
        self.add_to_response("result", result)
        self.add_to_response("time-to-serve", datetime.now() - start)
        
class Get_Detailed_Infos_For_Person_Model_WF(Base_Workflow):
    """
        For detailed displays purpose
        INPUT :
            person-type (actor, director, writer)
            person-id
        OUTPUT :
            thumbnail-url
            full-name
            nick-name
            alternate-names (not available for the moment)
            birth-name (not available for the moment)
            mini-story
            birth-date
            death-date
            place-of-birth
            place-of-death
            awards (won & nominated)
            movies (5 : thumbnail-url, release-date, original-title)
            slideshow (not available for the moment)
    """
    PERSON_TYPES = {u"actor" : "a", u"writer" : "b", u"director" : "c"}
    
    def __init__(self, input, authorization_pipe):
        Base_Workflow.__init__(self, input, authorization_pipe)
        
    def validate_input(self):
        self.validate_string_field_not_empty("person-type")
        self.validate_string_field_not_empty("person-id")
        
    def process(self):        
        person_type = self.request()["person-type"]
        person_id = self.request()["person-id"]
        
        if person_type not in Get_Detailed_Infos_For_Person_Model_WF.PERSON_TYPES.values(): person_type = None
        person_model = {
                'a': lambda person_id: Actor_Model.get_actor_model_by_id(id),
                'b': lambda person_id: Writer_Model.get_writer_model_by_id(id),
                'c': lambda person_id: Director_Model.get_director_model_by_id(id),
                'd': lambda person_id: None
                }[Get_Detailed_Infos_For_Person_Model_WF.PERSON_TYPES[person_type]](person_id)
        
        result = {}
        result["thumbnail-url"] = person_model.thumbnail_url
        result["full-name"] = person_model.full_name
        result["nick-name"] = person_model.nick_name
        result["mini-story"] = person_model.mini_story
        result["birth-date"] = person_model.birth_date
        result["death-date"] = person_model.death_date
        result["place-of-birth"] = person_model.place_of_birth
        result["place-of-death"] = person_model.place_of_death
        
        result["awards"] = []
        matchers = {
                'a': lambda person_model: Award_Matcher_Model.objects.filter(actor = person_model),
                'b': lambda person_model: Award_Matcher_Model.objects.filter(writer = person_model),
                'c': lambda person_model: Award_Matcher_Model.objects.filter(director = person_model),
                'd': lambda person_model: None
                }[Get_Detailed_Infos_For_Person_Model_WF.PERSON_TYPES[person_type]](person_model)
        award = {}
        for matcher in matchers:
            award["award"] = matcher.award.award_name
            award["award-status"] = matcher.award.award_status
            award["award-category"] = matcher.award_category.award_category_name
            award["movie"] = matcher.movie.original_title
        result["awards"].append(award)
        
        result["movies"] = []
        movies = {
                'a': lambda person_model: Movie_Model.objects.filter(actors = person_model)[:5],
                'b': lambda person_model: Movie_Model.objects.filter(writers = person_model)[:5],
                'c': lambda person_model: Movie_Model.objects.filter(directors = person_model)[:5],
                'd': lambda person_model: None
                }[Get_Detailed_Infos_For_Person_Model_WF.PERSON_TYPES[person_type]](person_model)
        movies_dict = {}
        if movies is not None:
            for movie in movies:
                movies_dict["original-title"] = movie.original_title
                movies_dict["release-date"] = movie.get_basic_release_date_for_movie()
                result["movies"].append(movies_dict)
        
        self.add_to_response("status", "ok")
        self.add_to_response("detailed-infos", result)

class Get_Detailed_Infos_For_Movie_Model_WF(Base_Workflow):
    """
        For detailed displays purpose
        INPUT :
            movie-id
        OUTPUT :
            status : "ok"
            detailed-infos : {
                original-title,
                genres,
                year-of-release,
                aka, (international_title, ~3)
                runtime,
                user-rating,
                directors, (1)
                actors, (3~4)
                plot,
                summary,
                thumbnail-url,
                oscars (won & nominated)
            }
    """
    def __init__(self, input, authorization_pipe):
        Base_Workflow.__init__(self, input, authorization_pipe)
        
    def validate_input(self):
        self.validate_string_field_not_empty("movie-id")
        
    def process(self):
        movie = Movie_Model.get_movie_model_by_id(self.request()["movie-id"])
        infos = {}
        
        # Easy-to-get infos
        infos["original-title"] = movie.original_title
        infos["runtime"] = movie.runtime
        infos["user-rating"] = movie.user_rating
        infos["thumbnail-url"] = movie.thumbnail_url
        infos["plot"] = movie.plot
        infos["summary"] = movie.summary
        
        # Returns the release date either of the USA, UK, or International release
        desired_release_dates = ["International", "USA", "UK", "France"]
        while infos["release-date"] is None:
            release_date_list = list(Release_Date_Model.objects.filter(related_movie =
                                self).filter(countries__country_name__iexact =
                                desired_release_dates.__iter__().next()))
            if release_date_list is not (None or []):
                infos["release-date"] = release_date_list[0].release_date
        if infos["release-date"] is None:
            infos["release-date"] = list(Release_Date_Model.objects.filter(related_movie = movie))[0]
        
        # Returns the list of the movie genres
        genres_list = []
        for genre in movie.genres.all():
            genres_list.append(genre.get_infos_for_model())
        infos["genres"] = genres_list
        
        # Returns the aka titles either of the USA, UK, or International release
        akas_dict = {}
        desired_akas = ["International", "USA", "UK", "France"]
        for string in desired_akas:
            aka_query = list(Aka_Model.objects.filter(related_movie = movie).filter(
                        countries__country_name__iexact = string))
            if aka_query is not (None or []):
                akas_dict[string] = aka_query[0].get_infos_for_model()
        infos["akas"] = akas_dict
        
        # Returns one of the movie film directors
#        directors_list = []
#        for director_model in movie.directors.all():
#            directors_list.append(director_model.get_infos_for_model())
        infos["director"] = list(movie.directors.all())[0].get_infos_for_model()
        
        # Returns x of the movie actors
        x = 4
        actors_query = Actor_Model.objects.filter(movie_model__in = [movie])[:x]
        actors_list = []
        for actor in actors_query:
            actors_list.append(actor.get_infos_for_model())
        infos["actors"] = actors_list
        
        # Returns the oscars for the movie
        oscars_list = []
        oscar_award = Award_Model.objects.filter(award_name__iexact = "Oscar")
        oscars_query = Award_Matcher_Model.objects.filter(award = oscar_award).filter(movie = movie)
        for match in oscars_query:
            oscars_list.append(match.award.get_infos_for_model())
        infos["oscars"] = oscars_list
        
        self.add_to_response("status", "ok")
        self.add_to_response("detailed-infos", infos)
    
class Store_Imdb_Object_WF(Base_Workflow):
    """
        Helps Jonas get some serialized imdb objects stored in
        seeker's tables
        INPUT :
            serialization-string
            filename
            extension
            path
            hashcode
            trailer-url
            trailer-width
            trailer-height
        OUPUT :
            status : "ok"
            imdb-model : an Imdb_Object_Model
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
        
    def validate_input(self):
        self.validate_string_field_not_empty("serialization-string")
        self.validate_string_field_not_empty("filename")
        self.validate_string_field_not_empty("extension")
        self.validate_string_field_not_empty("path")
        self.validate_string_field_not_empty("trailer-url")
        self.validate_string_field_not_empty("trailer-width")
        self.validate_string_field_not_empty("trailer-height")
        
    def process(self):
        serialization = self.request()["serialization-string"]
        filename = self.request()["filename"]
        extension = self.request()["extension"]
        path = self.request()["path"]
        hashcode = self.request()["hashcode"]
        trailer_url = self.request()["trailer-url"]
        width = self.request()["trailer-width"]
        height = self.request()["trailer-height"]
        
        model = Imdb_Object_Model.add_imdb_object_model(serialization, filename, extension,
                                                        path, hashcode, trailer_url, width, height)
        
        self.add_to_response("status", "ok")
        self.add_to_response("imdb-model", model)
        
class Create_Or_Get_Movie_WF(Base_Workflow):
    '''
        INPUT :
            imdb-id
            original-title
            filename
            extension
            path-on-disk
            hashcode
        OUTPUT :
            status : "ok"
            movie-model (a Movie_Model)
            already-existed (boolean)  
              
        BE AWARE : The models that are related to the Movie_Model (pk : movie-id)
        with a ManyToOneField (=ForeignKey) must be created AFTER the processing
        of this workflow, using the corresponding Create_Or_Get workflow and the
        movie-id rendered by this workflow.
        Otherwise, the Movie_Model (pk : movie-id) will lack its foreignkey related
        models (Complete_Movie_Model_WF DOES NOT take care of this particular type
        of relation)
    '''    
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("imdb-id")
#        self.string_cleaner("imdb-id")
        self.validate_string_field_not_empty("original-title")
#        self.string_cleaner("original-title")
        self.validate_string_field_not_empty("filename")
        # No cleaning on filename
        self.validate_string_field_not_empty("extension")
        # No cleaning on extension
        self.validate_string_field_not_empty("path-on-disk")
        # No cleaning on path-on-disk
        self.validate_string_field_not_empty("hashcode")
        self.string_cleaner("hashcode")
    
    def process(self):
        imdb_id = self.request()["imdb-id"]
        original_title = self.request()["original-title"]
        filename = self.request()["filename"]
        extension = self.request()["extension"]
        path_on_disk = self.request()["path-on-disk"]
        hash_code = self.request()["hashcode"]
        
        query = Movie_Model.get_movie_model_by_imdb_id(imdb_id)
        if query is None:
            already_existed = False
            movie_model = Movie_Model.add_movie_model(imdb_id, original_title, filename,
                                                      extension, path_on_disk, hash_code)
        else:
            already_existed = True
            movie_model = query
            
        self.add_to_response("status", "ok")
        self.add_to_response("movie-model", movie_model)
        self.add_to_response("already-existed", already_existed)

class Complete_Movie_Model_WF(Base_Workflow):
    """
        This workflow complete the movie model, adding all the ManyToManyField
        related models to the movie-model (which is a Movie_Model created by
        Create_Or_Get_Movie_WF)
    
        INPUT:
            runtime
            user-rating
            thumbnail-url
            plot
            summary
            movie-model : the movie model (got or created by Create_Or_Get_Movie_WF)
            original-countries : list of Country_Model
            actors : list of Actor_Model
            writers : list of Writer_Model
            directors : list of Director_Model
            genres : list of Genre_Model
        OUTPUT:
            status = "ok"
            movie-model
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("runtime")
        self.validate_string_field_not_empty("user-rating")
        self.validate_string_field_not_empty("thumbnail-url")
        self.validate_string_field_not_empty("plot")
        self.validate_string_field_not_empty("summary")
        self.validate_field_not_null("movie-model")
        self.validate_list_field_not_empty("original-countries")
        self.validate_list_field_not_empty("actors")
        self.validate_list_field_not_empty("writers")
        self.validate_list_field_not_empty("directors")
        self.validate_list_field_not_empty("genres")
    
    def process(self):
        movie_model = self.request()["movie-model"]                if self.validate_field_not_null("original-countries"):
            original_countries = self.request()["original-countries"]
        else: original_countries = None
        if self.validate_field_not_null("actors"):
            actors = self.request()["actors"]
        else: actors = None
        if self.validate_field_not_null("writers"):
            writers = self.request()["writers"]
        else: writers = None
        if self.validate_field_not_null("directors"):
            directors = self.request()["directors"]
        else: directors = None
        if self.validate_field_not_null("genres"):
            genres = self.request()["genres"]
        else: genres = None
        
        if original_countries is not None:
            movie_original_countries = movie_model.original_countries.all()
            for original_country in original_countries:
                if original_country not in movie_original_countries:
                    movie_model.original_countries.add(original_country)
        if actors is not None:
            movie_actors = movie_model.actors.all()
            for actor in actors:
                if actor not in movie_actors:
                    movie_model.actors.add(actor)
        if writers is not None:
            movie_writers = movie_model.writers.all()
            for writer in writers:
                if writer not in movie_writers:
                    movie_model.writers.add(writer)
        if directors is not None:
            movie_directors = movie_model.directors.all()
            for director in directors:
                if director not in movie_directors:
                    movie_model.directors.add(director)
        if genres is not None:
            movie_genres = movie_model.genres.all()
            for genre in genres:
                if genre not in movie_genres:
                    movie_model.genres.add(genre)

        movie_model = movie_model.add_some_more_infos(
                        self.request()["runtime"],
                        self.request()["user-rating"],
                        self.request()["thumbnail-url"],
                        self.request()["plot"],
                        self.request()["summary"])
        
        self.add_to_response("status", "ok")
        self.add_to_response("movie-model", movie_model)
    
class Create_Or_Get_Actor_WF(Base_Workflow):
    """
        INPUT:
            imdb-id
            full-name
            birth-date
            nick-name (optional)
            death-date (optional)
            mini-story (optional)
            thumbnail-url (optional)
        OUTPUT:
            status = "ok"
            actor-model (an Actor_Model)
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("imdb-id")
        self.string_cleaner("imdb-id")
        self.validate_string_field_not_empty("full-name")
        self.string_cleaner("full-name")
        self.validate_date_field("birth-date")
    
    def process(self):
        imdb_id = self.request()["imdb-id"]
        full_name = self.request()["full-name"]
        birth_date = self.request()["birth-date"]
        if self.validate_date_field("death-date"): death_date = self.request()["death-date"]
        else: death_date = None
        if self.validate_string_field_not_empty("nick-name"):
            self.string_cleaner("nick-name")
            nick_name = self.request()["nick-name"]
        else: nick_name = None
        if self.validate_string_field_not_empty("mini-story"): mini_story = self.request()["mini-story"]
        else: mini_story = None
        if self.validate_string_field_not_empty("thumbnail-url"): thumbnail_url = self.request()["thumbnail-url"]
        else: thumbnail_url = None
        
        query = Actor_Model.get_actor_model_by_imdb_id(imdb_id)
        if query is None:
            already_existed = False
            actor_model = Actor_Model.add_actor_model(imdb_id, full_name, birth_date, death_date,
                                                      nick_name, mini_story, thumbnail_url)
        else:
            already_existed = True
            actor_model = query
        
        self.add_to_response("status", "ok")
        self.add_to_response("actor-model", actor_model)
        self.add_to_response("already-existed", already_existed)
    
class Create_Or_Get_Writer_WF(Base_Workflow):
    """
        INPUT:
            imdb-id
            full-name
            birth-date
            nick-name (optional)
            death-date (optional)
            mini-story (optional)
            thumbnail-url (optional)
        OUTPUT:
            status = "ok"
            writer-model (a Writer_Model)
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("imdb-id")
        self.string_cleaner("imdb-id")
        self.validate_string_field_not_empty("full-name")
        self.string_cleaner("full-name")
        self.validate_date_field("birth-date")
    
    def process(self):
        imdb_id = self.request()["imdb-id"]
        full_name = self.request()["full-name"]
        birth_date = self.request()["birth-date"]
        if self.validate_date_field("death-date"): death_date = self.request()["death-date"]
        else: death_date = None
        if self.validate_string_field_not_empty("nick-name"):
            self.string_cleaner("nick-name")
            nick_name = self.request()["nick-name"]
        else: nick_name = None
        if self.validate_string_field_not_empty("mini-story"): mini_story = self.request()["mini-story"]
        else: mini_story = None
        if self.validate_string_field_not_empty("thumbnail-url"): thumbnail_url = self.request()["thumbnail-url"]
        else: thumbnail_url = None
        
        query = Writer_Model.get_writer_model_by_imdb_id(imdb_id)
        if query is None:
            already_existed = False
            writer_model = Writer_Model.add_writer_model(imdb_id, full_name, birth_date, death_date,
                                                         nick_name, mini_story, thumbnail_url)
        else:
            already_existed = True
            writer_model = query
        
        self.add_to_response("status", "ok")
        self.add_to_response("writer-model", writer_model)
        self.add_to_response("already-existed", already_existed)
    
class Create_Or_Get_Director_WF(Base_Workflow):
    """
        INPUT:
            imdb-id
            full-name
            birth-date
            nick-name (optional)
            death-date (optional)
        OUTPUT:
            status = "ok"
            director-model (a Director_Model)
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("imdb-id")
        self.string_cleaner("imdb-id")
        self.validate_string_field_not_empty("full-name")
        self.string_cleaner("full-name")
        self.validate_date_field("birth-date")
    
    def process(self):
        imdb_id = self.request()["imdb-id"]
        full_name = self.request()["full-name"]
        birth_date = self.request()["birth-date"]
        if self.validate_date_field("death-date"): death_date = self.request()["death-date"]
        else: death_date = None
        if self.validate_string_field_not_empty("nick-name"):
            self.string_cleaner("nick-name")
            nick_name = self.request()["nick-name"]
        else: nick_name = None
        if self.validate_string_field_not_empty("mini-story"): mini_story = self.request()["mini-story"]
        else: mini_story = None
        if self.validate_string_field_not_empty("thumbnail-url"): thumbnail_url = self.request()["thumbnail-url"]
        else: thumbnail_url = None
        
        query = Director_Model.get_director_model_by_imdb_id(imdb_id)
        if query is None:
            already_existed = False
            director_model = Director_Model.add_director_model(imdb_id, full_name, birth_date, death_date,
                                                               nick_name, mini_story, thumbnail_url)
        else:
            already_existed = True
            director_model = query
        
        self.add_to_response("status", "ok")
        self.add_to_response("director-model", director_model)
        self.add_to_response("already-existed", already_existed)
    
class Create_Or_Get_Country_WF(Base_Workflow):
    """
        INPUT:
            country-name
        OUTPUT:
            status = "ok"
            country-model
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("country-name")
        self.string_cleaner("country-name")
    
    def process(self):
        country_name = self.request()["country-name"]
        
        query = Country_Model.get_country_model(country_name)
        if query is None:
            already_existed = False
            country_model = Country_Model.add_country_model(country_name)
        else:
            already_existed = True
            country_model = query
            
        self.add_to_response("status", "ok")
        self.add_to_response("country-model", country_model)
        self.add_to_response("already-existed", already_existed)

class Create_Or_Get_Award_Category_WF(Base_Workflow):
    """
        INPUT:
            award-category-name
        OUTPUT:
            status = "ok"
            award-category-model (an Award_Category_Model)
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("award-category-name")
        self.string_cleaner("award-category-name")
    
    def process(self):
        award_category_name = self.request()["award-category-name"]
        
        query = Award_Category_Model.get_award_category_model(award_category_name)
        if query is None:
            already_existed = False
            award_category_model = Award_Category_Model.add_award_category_model(award_category_name)
        else:
            already_existed = True
            award_category_model = query
        
        self.add_to_response("status", "ok")
        self.add_to_response("award-category-model", award_category_model)
        self.add_to_response("already-existed", already_existed)
   
class Create_Or_Get_Award_WF(Base_Workflow):
    """
        INPUT : 
            DIRECT INPUT:
                award-name
                date-of-awarding
                award-status (see Award_Model.STATUSES)
        OUTPUT:
            status = "ok"
            award-model
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("award-name")
#        self.string_cleaner("award-name")
        self.validate_string_field_not_empty("award-status")
#        self.string_cleaner("award-status")
        self.validate_date_field("date-of-awarding")
    
    def process(self):
        award_name = self.request()["award-name"]
        date_of_awarding = self.request()["date-of-awarding"]
        award_status = self.request()["award-status"]
        if self.validate_list_field_not_empty("award-categories"): award_categories = self.request()["award-categories"]
        else: award_categories = None
        
        query = Award_Model.get_award_model(award_name, date_of_awarding, award_status)
        if query is None:
            already_existed = False
            award_model = Award_Model.add_award_model(award_name, date_of_awarding, award_status)
        else:
            already_existed = True
            award_model = query
        
        self.add_to_response("status", "ok")
        self.add_to_response("award-model", award_model)
        self.add_to_response("already-existed", already_existed)
        
class Create_Or_Get_Genre_WF(Base_Workflow):
    """
        INPUT:
            genre-name
        OUTPUT:
            status = "ok"
            genre-model (a Genre_Model)
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("genre-name")
#        self.string_cleaner("genre-name")
    
    def process(self):
        genre_name = self.request()["genre-name"]
        
        query = Genre_Model.get_genre_model(genre_name)
        if query is None:
            already_existed = False
            genre_model = Genre_Model.add_genre_model(genre_name)
        else:
            already_existed = True
            genre_model = query
            
        self.add_to_response("status", "ok")
        self.add_to_response("genre-model", genre_model)
        self.add_to_response("already-existed", already_existed)
        
class Create_Or_Get_Character_WF(Base_Workflow):
    """
        DIRECT INPUT:
            imdb-id
            character-name
            related-actor (an Actor_Model)
            related-movie (a Movie_Model)
        OUTPUT:
            status = "ok"
            character-model (a Character_Model)
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("character-name")
#        self.string_cleaner("character-name")
        self.validate_field_not_null("related-actor")
        self.validate_field_not_null("related-movie")
        self.validate_string_field_not_empty("imdb-id")
    
    def process(self):
        imdb_id = self.request()["imdb-id"]
        character_name = self.request()["character-name"]
        related_actor = self.request()["related-actor"]
        related_movie = self.request()["related-movie"]
        
        query = Character_Model.get_character_model_by_imdb_id(imdb_id)
        if query is None:
            already_existed = False
            character_model = Character_Model.add_character_model(imdb_id, character_name,
                                                                  related_actor, related_movie)
        else:
            already_existed = True
            character_model = query
            
        self.add_to_response("status", "ok")
        self.add_to_response("character-model", character_model)
        self.add_to_response("already-existed", already_existed)

class Create_Or_Get_Synopsis_WF(Base_Workflow):
    """
        INPUT :
            DIRECT INPUT :
                plain-text
            RELATED INPUT :
                movie-model
                country-models (a list of Country_Model)
        OUTPUT :
            status : "ok"
            synopsis-model (a Synopsis_Model)
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("plain-text")
        # No control on that input !
        self.validate_field_not_null("movie-model")
        self.validate_list_field_not_empty("country-models")
    
    def process(self):
        plain_text = self.request()["plain-text"]
        movie_model = self.request()["movie-model"]
        country_models = self.request()["country-models"]
                
        query = self.repository().get_synopsis_model(movie_model, country_models)
        if query is None:
            already_existed = False
            synopsis_model = Synopsis_Model.add_synopsis_model(plain_text, movie_model)
            synopsis_model = self.repository().add_countries(synopsis_model, country_models)
        else:
            already_existed = True
            synopsis_model = query

        self.add_to_response("status", "ok")
        self.add_to_response("synopsis-model", synopsis_model)
        self.add_to_response("already-existed", already_existed)

class Create_Or_Get_Aka_WF(Base_Workflow):
    """
        INPUT :
            DIRECT INPUT :
                aka-name
            RELATED INPUT :
                movie-model (a Movie_Model)
                country-models (a list of Country_Model)
        OUTPUT :
            status : "ok"
            aka-model : an Aka_Model
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_string_field_not_empty("aka-name")
        self.string_cleaner("aka-name")
        self.validate_field_not_null("movie-model")
        self.validate_list_field_not_empty("country-models")
    
    def process(self):
        aka_name = self.request()["aka-name"]
        movie_model = self.request()["movie-model"]
        country_models = self.request()["country-models"]
        
        query = Aka_Model.get_aka_model(aka_name)
        if query is None:
            already_existed = False
            aka_model = Aka_Model.add_aka_model(aka_name, movie_model)
            aka_model = self.repository().add_countries(aka_model, country_models)
        else:
            already_existed = True
            aka_model = query

        self.add_to_response("status", "ok")
        self.add_to_response("aka-model", aka_model)
        self.add_to_response("already-existed", already_existed)

class Create_Or_Get_Release_Date_WF(Base_Workflow):
    """
        INPUT :
            DIRECT INPUT :
                release-date
            RELATED INPUT :
                movie-model (a Movie_Model)
                country-models (a list of Country_Model)
        OUTPUT :
            status : "ok"
            release-date-model (a Release_Date_Model)
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
    
    def validate_input(self):
        self.validate_date_field("release-date")
        self.validate_field_not_null("movie-model")
        self.validate_list_field_not_empty("country-models")
    
    def process(self):
        release_date = self.request()["release-date"]
        movie_model = self.request()["movie-model"]
        country_models = self.request()["country-models"]
        
        query = self.repository().get_release_date_model(movie_model, country_models)
        if query is None:
            already_existed = False
            release_date_model = Release_Date_Model.add_release_date_model(release_date, movie_model)
            release_date_model = self.repository().add_countries(release_date_model, country_models)
        else:
            already_existed = True
            release_date_model = query

        self.add_to_response("status", "ok")
        self.add_to_response("release-date-model", release_date_model)
        self.add_to_response("already-existed", already_existed)
        
class Create_Or_Get_Award_Matcher_WF(Base_Workflow):
    """
        Binds the models related to awards together
        BE AWARE : actor-model, director-model, writer-model are
        optional, while for instance a staff director can
        pretend to an award... Those person categories are not
        taken in account by the modeling we've made.
        
        INPUT :
            movie-model
            award-model
            award-category-model
            actor-model (optional)
            director-model (optional)
            writer-model (optional)
        OUTPUT :
            status : "ok"
            award-manager-model
            already-existed (boolean)
    """
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization)
        
    def validate_input(self):
        self.validate_field_not_null("movie-model")
        self.validate_field_not_null("award-model")
        self.validate_field_not_null("award-category-model")
    
    def process(self):
        movie_model = self.request()["movie-model"]
        award_model = self.request()["award-model"]
        award_category_model = self.request()["award-category-model"]
        if self.validate_field_not_null("actor-model"):
            actor_model = self.request()["actor-model"]
        else: actor_model = None
        if self.validate_field_not_null("director-model"):
            director_model = self.request()["director-model"]
        else: director_model = None
        if self.validate_field_not_null("writer-model"):
            writer_model = self.request()["writer-model"]
        else: writer_model = None
        
        query = Award_Matcher_Model.get_award_matcher(movie_model, actor_model, director_model,
                                                      writer_model, award_model, award_category_model)
        if query is None:
            already_existed = False
            award_matcher_model = Award_Matcher_Model.add_award_matcher_model(movie_model,
                                                                              actor_model,
                                                                              director_model,
                                                                              writer_model,
                                                                              award_model,
                                                                              award_category_model)
        else:
            already_existed = True
            award_matcher_model = query
        
        self.add_to_response("status", "ok")
        self.add_to_response("award-matcher-model", award_matcher_model)
        self.add_to_response("already-existed", already_existed)
        
class Create_Fake_Movie_WF(Base_Workflow):
    """
        Faker to test models creation
        INPUT : 
            None
        OUTPUT :
            status : "ok"
            movie-model (a Movie_Model)
            already-existed
            time-to-serve
    """
    def __init__(self, input, authorization_pipe):
        Base_Workflow.__init__(self, input, authorization_pipe)
        
    def validate_input(self):
        pass
    
    def process(self):
        from datetime import time, date, datetime
        start = datetime.now()
        
        movie_imdb_id = "MOVIE_IMDB_ID"
        result = Create_Or_Get_Movie_WF({"imdb-id" : movie_imdb_id,
                                         "original-title" : "My Favourite Movie",
                                         "filename" : "My Favourite Movie.avi",
                                         "extension" : ".avi",
                                         "path-on-disk" : "Z:\\Movies\\",
                                         "hashcode" : "ipno8970982nnuiyno76987"},
                                         None).work()
        movie_model = result["movie-model"]
        
        if not result["already-existed"]:
            actor_imdb_id_1 = "ACTOR_IMDB_ID_1"
            if Actor_Model.get_actor_model_by_imdb_id(actor_imdb_id_1) is None:
                actor_1 = Create_Or_Get_Actor_WF({"imdb-id" : actor_imdb_id_1,
                                                  "full-name" : "John Actor",
                                                  "birth-date" : date(1964,3,7),
                                                  "nick-name" : "Actor One",
                                                  "death-date" : None,
                                                  "mini-story" : "blabla",
                                                  "thumbnail-url" : "http://image.com"
                                                  }, None).work()["actor-model"]
            actor_imdb_id_2 = "ACTOR_IMDB_ID_2"
            if Actor_Model.get_actor_model_by_imdb_id(actor_imdb_id_2) is None:
                actor_2 = Create_Or_Get_Actor_WF({"imdb-id" : actor_imdb_id_2,
                                                  "full-name" : "John Actress",
                                                  "birth-date" : date(1975,5,10),
                                                  "nick-name" : "Actor Two",
                                                  "mini-story" : "blabla",
                                                  "thumbnail-url" : "http://image.com"
                                                  }, None).work()["actor-model"]
            
            writer_imdb_id_1 = "WRITER_IMDB_ID_1"
            if Writer_Model.get_writer_model_by_imdb_id(writer_imdb_id_1) is None:
                writer_1 = Create_Or_Get_Writer_WF({"imdb-id" : writer_imdb_id_1,
                                                    "full-name" : "John Writer",
                                                    "birth-date" : date(1974,2,10),
                                                    "nick-name" : "Writer One",
                                                    "death-date" : None,
                                                    "mini-story" : "blabla",
                                                    "thumbnail-url" : "http://image.com"
                                                    }, None).work()["writer-model"]

            writer_imdb_id_2 = "WRITER_IMDB_ID_2"
            if Writer_Model.get_writer_model_by_imdb_id(writer_imdb_id_2) is None:
                writer_2 = Create_Or_Get_Writer_WF({"imdb-id" : writer_imdb_id_2,
                                                    "full-name" : "John Writress",
                                                    "birth-date" : date(1974,1,10),
                                                    "nick-name" : "Writer Two",
                                                    "death-date" : None,
                                                    "mini-story" : "blabla",
                                                    "thumbnail-url" : "http://image.com"
                                                    }, None).work()["writer-model"]
            
            director_imdb_id_1 = "DIRECTOR_IMDB_ID_1"
            if Director_Model.get_director_model_by_imdb_id(director_imdb_id_1) is None:                               
                director_1 = Create_Or_Get_Director_WF({"imdb-id" : director_imdb_id_1,
                                                        "full-name" : "John Director",
                                                        "birth-date" : date(1954,2,10),
                                                        "nick-name" : "Director One",
                                                        "death-date" : None,
                                                        "mini-story" : "blabla",
                                                        "thumbnail-url" : "http://image.com"
                                                        }, None).work()["director-model"]
                                     
            director_imdb_id_2 = "DIRECTOR_IMDB_ID_2"
            if Director_Model.get_director_model_by_imdb_id(id) is None:
                director_2 = Create_Or_Get_Director_WF({"imdb-id" : director_imdb_id_2,
                                                        "full-name" : "John Directress",
                                                        "birth-date" : date(1978,2,10),
                                                        "death-date" : None,
                                                        "mini-story" : "blabla",
                                                        "thumbnail-url" : "http://image.com"
                                                        }, None).work()["director-model"]
            
            country_1 = Create_Or_Get_Country_WF({"country-name" : "France"}, None).work()["country-model"]
            country_2 = Create_Or_Get_Country_WF({"country-name" : "Germany"}, None).work()["country-model"]
            country_3 = Create_Or_Get_Country_WF({"country-name" : "Marocco"}, None).work()["country-model"]
            country_4 = Create_Or_Get_Country_WF({"country-name" : "China"}, None).work()["country-model"]
            country_5 = Create_Or_Get_Country_WF({"country-name" : "Italia"}, None).work()["country-model"]
            
            award_category_1 = Create_Or_Get_Award_Category_WF({"award-category-name" : "Best Actor Ever"},
                                                               None).work()["award-category-model"]
            award_category_2 = Create_Or_Get_Award_Category_WF({"award-category-name" : "Best Failure Ever"},
                                                               None).work()["award-category-model"]
    
            award_imdb_id_1 = "AWARD_IMDB_ID_1"
            award_1 = Create_Or_Get_Award_WF({"award-name" : "Bafta",
                                              "date-of-awarding" : date(2005,6,3),
                                              "award-status" : "Won"}, None).work()["award-model"]

            award_imdb_id_2 = "AWARD_IMDB_ID_2"
            award_2 = Create_Or_Get_Award_WF({"award-name" : "Oscar",
                                              "date-of-awarding" : date(2005,6,3),
                                              "award-status" : "Nominated"}, None).work()["award-model"]
            
            genre_1 = Create_Or_Get_Genre_WF({"genre-name" : "action"}, None).work()["genre-model"]
            genre_2 = Create_Or_Get_Genre_WF({"genre-name" : "romance"}, None).work()["genre-model"]
            
            character_imdb_id_1 = "CHARACTER_IMDB_ID_1"
            if Character_Model.get_character_model_by_imdb_id(character_imdb_id_1) is None:
                character_1 = Create_Or_Get_Character_WF({"imdb-id" : character_imdb_id_1,
                                                          "character-name" : "Godzilla",
                                                          "related-actor" : actor_1,
                                                          "related-movie" : movie_model},
                                                          None).work()["character-model"]  
            character_imdb_id_2 = "CHARACTER_IMDB_ID_2"
            if Character_Model.get_character_model_by_imdb_id(character_imdb_id_2) is None:
                character_2 = Create_Or_Get_Character_WF({"imdb-id" : character_imdb_id_2,
                                                          "character-name" : "Pocahontas",
                                                          "related-actor" : actor_2,
                                                          "related-movie" : movie_model},
                                                          None).work()["character-model"]
                                                      
#            synopsis_1 = Create_Or_Get_Synopsis_WF({"plain-text" : "First synopsis of this crazy movie!",
#                                                    "movie-model" : movie_model,
#                                                    "country-models" : [country_1, country_2]}, None).work()["synopsis-model"]                                          
#            synopsis_2 = Create_Or_Get_Synopsis_WF({"plain-text" : "Second synopsis of the 'My Favourite Movie'!",
#                                                    "movie-model" : movie_model,
#                                                    "country-models" : [country_3, country_4, country_5]}, None).work()["synopsis-model"]
                                                    
            aka_1 = Create_Or_Get_Aka_WF({"aka-name" : "Fatal Love Disruptor",
                                          "movie-model" : movie_model,
                                          "country-models" : [country_2, country_3]}, None).work()["aka-model"]                                       
            aka_2 = Create_Or_Get_Aka_WF({"aka-name" : "Chuck Norris Could Cry",
                                          "movie-model" : movie_model,
                                          "country-models" : [country_1]}, None).work()["aka-model"]
                                          
            release_date_1 = Create_Or_Get_Release_Date_WF({"release-date" : date(2009,5,11),
                                                            "movie-model" : movie_model,
                                                            "country-models" : [country_4, country_5]}, None).work()["release-date-model"]                              
            release_date_2 = Create_Or_Get_Release_Date_WF({"release-date" : date(2009,8,11),
                                                            "movie-model" : movie_model,
                                                            "country-models" : [country_1, country_2]}, None).work()["release-date-model"]
                                                            
            Create_Or_Get_Award_Matcher_WF({"movie-model" : movie_model,
                                            "award-model" : award_1,
                                            "award-category-model" : award_category_1,
                                            "actor-model" : actor_1,
                                            "director-model" : None,
                                            "writer-model" : None},
                                            None).work()                                          
            Create_Or_Get_Award_Matcher_WF({"movie-model" : movie_model,
                                            "award-model" : award_2,
                                            "award-category-model" : award_category_1,
                                            "actor-model" : actor_2,
                                            "director-model" : None,
                                            "writer-model" : None},
                                            None).work()                                        
            Create_Or_Get_Award_Matcher_WF({"movie-model" : movie_model,
                                            "award-model" : award_1,
                                            "award-category-model" : award_category_2,
                                            "actor-model" : None,
                                            "director-model" : None,
                                            "writer-model" : None},
                                            None).work()                                 
            Create_Or_Get_Award_Matcher_WF({"movie-model" : movie_model,
                                            "award-model" : award_2,
                                            "award-category-model" : award_category_2,
                                            "actor-model" : actor_1,
                                            "director-model" : None,
                                            "writer-model" : None},
                                            None).work()
            
            complete_movie_model = Complete_Movie_Model_WF({
                                            "runtime" : "2:24",
                                            "user-rating" : "8.6",
                                            "thumbnail-url" : "http://www.t-site.com/my_favourite_movie/thumbnail.png",
                                            "plot" : "plot_blabla",
                                            "summary" : "summary_blabla",
                                            "movie-model" : movie_model,
                                            "original-countries" : [country_1, country_2, country_3, country_4, country_5],
                                            "actors" : [actor_1, actor_2],
                                            "writers" : [writer_1, writer_2],
                                            "directors" : [director_1, director_2],
                                            "genres" : [genre_1, genre_2]},
                                            None).work()["movie-model"]
        
        self.add_to_response("status", "ok")
        self.add_to_response("movie-model", movie_model)
        self.add_to_response("already-existed", result["already-existed"])
        self.add_to_response("time-to-serve", datetime.now() - start)
