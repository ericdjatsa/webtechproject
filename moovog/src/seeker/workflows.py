'''
Created on 19 avr. 2010
@author: Christophe

This file gather all together the logic behind the views
'''

from base.Base_Workflow import Base_Workflow
from src.seeker.models import *

import logging

class General_Search_WF(Base_Workflow):
    '''    GENERAL SEARCH
        INPUT :
            search string
            
        OUTPUT :
            list of models that correspond to the search
    '''
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        pass
    
    def process(self):
        to_search = self.request()["search-bar"]
        
        result_movie_list = []
        # go and find into the models
        
        pass

class Create_Or_Get_Movie_WF(Base_Workflow):
    '''
        INPUT :
            original-title
            runtime
            user-rating
            thumbnail
            filename
            extension
            path
            md5
        OUTPUT :
            status : "ok"
            movie-id
            already-created (boolean)  
              
        BE AWARE : The models that are related to the Movie_Model (pk : movie-id)
        with a ManyToOneField (=ForeignKey) must be created AFTER the processing
        of this workflow, using the corresponding Create_Or_Get workflow and the
        movie-id rendered by this workflow.
        Otherwise, the Movie_Model (pk : movie-id) will lack its foreignkey related
        models (Complete_Movie_Model_WF DOES NOT take care of this particular type
        of relation)
    '''    
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("original-title")
        self.validate_time_field("runtime")
        self.validate_string_field_not_empty("user-rating")
        self.validate_string_field_not_empty("thumbnail-url")
        self.validate_string_field_not_empty("filename")
        self.validate_string_field_not_empty("extension")
        self.validate_string_field_not_empty("path-on-disk")
        self.validate_string_field_not_empty("hashcode")
    
    def process(self):
        original_title = self.request()["original-title"]
        runtime = self.request()["runtime"]
        user_rating = self.request()["user-rating"]
        thumbnail_url = self.request()["thumbnail-url"]
        filename = self.request()["filename"]
        extension = self.request()["extension"]
        path_on_disk = self.request()["path-on-disk"]
        hash_code = self.request()["hashcode"]
        
        query = Movie_Model.get_movie_model(filename, extension, path_on_disk, hash_code)
        if query is None:
            already_existed = False
            movie = Movie_Model.add_movie_model(original_title, duration, user_rating, thumbnail_url,
                                                filename, extension, path_on_disk, hash_code)
            movie_id = movie.id
        else:
            already_existed = True
            movie_id = query.id
            
        self.add_to_response("status", "ok")
        self.add_to_response("movie-id", movie_id)
        self.add_to_response("already-existed", already_existed)

class Complete_Movie_Model_WF(Base_Workflow):
    """
        This workflow complete the movie model, adding all the ManyToManyField
        related models to the beneath the Movie_Model which primary key is movie-id
    
        INPUT:
            movie-id : id of the movie (got or created by Create_Or_Get_Movie_WF)
            original-countries : list of Country_Model
            awards : list of Award_Model
            characters : list of Character_Model
            actors : list of Actor_Model
            writers : list of Writer_Model
            directors : list of Director_Model
            genres : list of Genre_Model
        OUTPUT:
            status = "ok"
            movie-id
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("movie-id")
    
    def process(self):
        movie_id = self.request()["movie-id"]
        
        if self.validate_field_not_null("original-countries"):
            original_countries = self.request()["original-countries"]
        else: original_countries = None
        if self.validate_field_not_null("awards"):
            awards = self.request()["awards"]
        else: awards = None
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
        
        movie = Movie_Model.get_movie_model_by_id(movie_id)
        if original_countries is not None:
            movie_original_countries = movie.original_countries.all()
            for original_country in original_countries:
                if original_country not in movie_original_countries:
                    movie.original_countries.add(original_country)
        if awards is not None:
            movie_awards = movie.awards.all()
            for award in awards:
                if award not in movie_awards:
                    movie.awards.add(award)
        if actors is not None:
            movie_actors = movie.actors.all()
            for actor in actors:
                if actor not in movie_actors:
                    movie.actors.add(actor)
        if writers is not None:
            movie_writers = movie.writers.all()
            for writer in writers:
                if writer not in movie_writers:
                    movie.writers.add(writer)
        if directors is not None:
            movie_directors = movie.directors.all()
            for director in directors:
                if director not in movie_directors:
                    movie.directors.add(director)
        if genres is not None:
            movie_genres = movie.genres.all()
            for genre in genres:
                if genre not in movie_genres:
                    movie.genres.add(genre)
        
        self.add_to_response("status", "ok")
        self.add_to_response("actor-id", movie_id)
    
class Create_Or_Get_Actor_WF(Base_Workflow):
    """
        INPUT:
            first-name
            last-name
            birth-date
            nick-name (optional)
            death-date (optional)
            awards (optional, list of Award_Model)
        OUTPUT:
            status = "ok"
            actor_id
            already-existed (boolean)
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("first-name")
        self.validate_string_field_not_empty("last-name")
        self.validate_date_field("birth-date")
    
    def process(self):
        first_name = self.request()["first-name"]
        last_name = self.request()["last-name"]
        birth_date = self.request()["birth_date"]
        if self.validate_date_field("death-date"): death_date = self.request()["death-date"]
        else: death_date = None
        if self.validate_string_field_not_empty("nick-name"): nick_name = self.request()["nick-name"]
        else: nick_name = None
        if self.validate_field_not_null("awards"): awards = self.request()["awards"]
        else: awards = None
        
        query = Actor_Model.get_actor_model(first_name, last_name, birth_date)
        if query is None:
            already_existed = False
            actor = Actor_Model.add_actor_model(first_name, last_name, birth_date, death_date, nick_name)
            if awards is not None:
                self.repository().add_awards(actor, awards)
            actor_id = actor.id
        else:
            already_existed = True
            actor_id = query.id
        
        self.add_to_response("status", "ok")
        self.add_to_response("actor-id", actor_id)
        self.add_to_response("already-existed", already_existed)
    
class Create_Or_Get_Writer_WF(Base_Workflow):
    """
        INPUT:
            first-name
            last-name
            birth-date
            nick-name (optional)
            death-date (optional)
            awards (optional, list of Award_Model)
        OUTPUT:
            status = "ok"
            writer_id
            already-existed (boolean)
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("first-name")
        self.validate_string_field_not_empty("last-name")
        self.validate_date_field("birth-date")
    
    def process(self):
        first_name = self.request()["first-name"]
        last_name = self.request()["last-name"]
        birth_date = self.request()["birth_date"]
        if self.validate_date_field("death-date"): death_date = self.request()["death-date"]
        else: death_date = None
        if self.validate_string_field_not_empty("nick-name"): nick_name = self.request()["nick-name"]
        else: nick_name = None
        if self.validate_field_not_null("awards"): awards = self.request()["awards"]
        else: awards = None
        
        query = Writer_Model.get_writer_model(first_name, last_name, birth_date)
        if query is None:
            already_existed = False
            writer = Writer_Model.add_writer_model(first_name, last_name, birth_date, death_date, nick_name)
            if awards is not None:
                self.repository().add_awards(writer, awards)
            writer_id = writer.id
        else:
            already_existed = True
            writer_id = query.id
        
        self.add_to_response("status", "ok")
        self.add_to_response("writer-id", writer_id)
        self.add_to_response("already-existed", already_existed)
    
class Create_Or_Get_Director_WF(Base_Workflow):
    """
        INPUT:
            first-name
            last-name
            birth-date
            nick-name (optional)
            death-date (optional)
            awards (optional, list of Award_Model)
        OUTPUT:
            status = "ok"
            director_id
            already-existed (boolean)
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("first-name")
        self.validate_string_field_not_empty("last-name")
        self.validate_date_field("birth-date")
    
    def process(self):
        first_name = self.request()["first-name"]
        last_name = self.request()["last-name"]
        birth_date = self.request()["birth_date"]
        if self.validate_date_field("death-date"): death_date = self.request()["death-date"]
        else: death_date = None
        if self.validate_string_field_not_empty("nick-name"): nick_name = self.request()["nick-name"]
        else: nick_name = None
        if self.validate_field_not_null("awards"): awards = self.request()["awards"]
        else: awards = None
        
        query = Director_Model.get_director_model(first_name, last_name, birth_date)
        if query is None:
            already_existed = False
            director = Director_Model.add_director_model(first_name, last_name, birth_date, death_date, nick_name)
            if awards is not None:
                self.repository().add_awards(director, awards)
            director_id = director.id
        else:
            already_existed = True
            director_id = query.id
        
        self.add_to_response("status", "ok")
        self.add_to_response("director-id", director_id)
        self.add_to_response("already-existed", already_existed)
    
class Create_Or_Get_Country_WF(Base_Workflow):
    """
        INPUT:
            country-name
        OUTPUT:
            status = "ok"
            country-id
            already-existed (boolean)
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("country-name")
    
    def process(self):
        country_name = self.request()["country-name"]
        
        query = Country_Model.get_country_model(country_name)
        if query is None:
            already_existed = False
            country = Country_Model.add_country_model(country_name)
            country_id = country.id
        else:
            already_existed = True
            country_id = query.id
            
        self.add_to_response("status", "ok")
        self.add_to_response("country-id", country_id)
        self.add_to_response("already-existed", already_existed)

class Create_Or_Get_Award_Category_WF(Base_Workflow):
    """
        INPUT:
            award-category-name
        OUTPUT:
            status = "ok"
            award-category-id
            already-existed (boolean)
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("award-category-name")
    
    def process(self):
        award_category_name = self.request()["award-category-name"]
        
        query = Award_Category_Model.get_award_category_model(award_category_name)
        if query is None:
            already_existed = False
            award_category = Award_Category_Model.add_award_category_model(award_category_name)
            award_category_id = award_category.id
        else:
            already_existed = True
            award_category_id = query.id
        
        self.add_to_response("status", "ok")
        self.add_to_response("award-category-id", award_category_id)
        self.add_to_response("already-existed", already_existed)
   
class Create_Or_Get_Award_WF(Base_Workflow):
    """
        DIRECT INPUT:
            award-name
            date-of-awarding
            award-status (string, see Award_Model.STATUSES)
        RELATED INPUT:
            award-categories (list of Award_Category_Model)
        OUTPUT:
            status = "ok"
            award-id
            already-existed (boolean)
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("award-name")
        self.validate_date_field("date-of-awarding")
        self.validate_string_field_not_empty("award-status")
    
    def process(self):
        award_name = self.request()["award-name"]
        date_of_awarding = self.request()["date-of-awarding"]
        award_status = self.request()["award-status"]
        if self.validate_string_field_not_empty("award-categories"): award_categories = self.request()["award-categories"]
        else: award_categories = None
        
        query = Award_Model.get_award_model(award_name, date_of_awarding)
        if query is None:
            already_existed = False
            award = Award_Model.add_award_model(award_name, date_of_awarding, award_status)
            award = self.repository().add_award_categories(award, award_categories)
            award_id = award.id
        else:
            already_existed = True
            award_id = query.id
        
        self.add_to_response("status", "ok")
        self.add_to_response("award-category-id", award_id)
        self.add_to_response("already-existed", already_existed)
        
class Create_Or_Get_Genre_WF(Base_Workflow):
    """
        INPUT:
            genre-name
        OUTPUT:
            status = "ok"
            country-id
            already-existed (boolean)
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("genre-name")
    
    def process(self):
        genre_name = self.request()["genre-name"]
        
        query = Genre_Model.get_genre_model(genre_name)
        if query is None:
            already_existed = False
            genre = Genre_Model.add_genre_model(genre_name)
            genre_id = genre.id
        else:
            already_existed = True
            genre_id = query.id
            
        self.add_to_response("status", "ok")
        self.add_to_response("genre-id", genre_id)
        self.add_to_response("already-existed", already_existed)
        
class Create_Or_Get_Character_WF(Base_Workflow):
    """
        DIRECT INPUT:
            character-name
        RELATED INPUT:
            related-actors (list of Actor_Model)
            related-movies (list of Movie_Model)
        OUTPUT:
            status = "ok"
            country-id
            already-existed (boolean)
    """
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("character-name")
        self.validate_field_not_null("related-actors")
        self.validate_field_not_null("related-movies")
    
    def process(self):
        genre_name = self.request()["genre-name"]
        related_actors = self.request()["related-actors"]
        related_movies = self.request()["related-movies"]
        
        query = Character_Model.get_character_model(character_name)
        if query is None:
            already_existed = False
            genre = Genre_Model.add_genre_model(genre_name)
            genre_id = genre.id
        else:
            already_existed = True
            genre_id = query.id
            
        self.add_to_response("status", "ok")
        self.add_to_response("genre-id", genre_id)
        self.add_to_response("already-existed", already_existed)
        
class Create_Or_Get_Aka_WF(Base_Workflow):
    pass

class Create_Or_Get_Release_Date_WF(Base_Workflow):
    pass