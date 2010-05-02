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
        
        return result_movie_list
    
class Find_Movie_By_Actor_WF(Base_Workflow):
    pass

class Find_Actor_WF(Base_Workflow):
    pass

class Find_Director_WF(Base_Workflow):
    pass

class Find_Writer_WF(Base_Workflow):
    pass

class Create_Or_Get_Movie_WF(Base_Workflow):
    '''
        INPUT :
            DIRECT INPUTS :
                original_title
                runtime
                user_rating
                thumbnail
                filename
                extension
                path
                md5
            RELATED INPUTS :
                original_countries : list of Country_Model
                akas : list of Aka_Model
                characters : list of Character_Model
                actors : list of Actor_Model
                writers : list of Writer_Model
                directors : list of Director_Model
                release_dates : list of Release_Date_Model
                synopsises : list of Synopsis_Model
                genres : list of Genre_Model
        OUTPUT :
            status : "ok"
            movie model id
            already_created (boolean)
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
        self.validate_string_field_not_empty("md5")
    
    def process(self):
        original_title = self.request()["original-title"]
        runtime = self.request()["runtime"]
        user_rating = self.request()["user-rating"]
        thumbnail_url = self.request()["thumbnail-url"]
        filename = self.request()["filename"]
        extension = self.request()["extension"]
        path_on_disk = self.request()["path-on-disk"]
        md5 = self.request()["md5"]
        if self.validate_field_not_null("original-countries"): original_countries = self.request()["original-countries"]
        else: original_countries = None
        if self.validate_field_not_null("akas"): akas = self.request()["akas"]
        else: akas = None
        if self.validate_field_not_null("characters"): characters = self.request()["characters"]
        else: characters = None
        if self.validate_field_not_null("actors"): actors = self.request()["actors"]
        else: actors = None
        if self.validate_field_not_null("writers"): writers = self.request()["writers"]
        else: writers = None
        if self.validate_field_not_null("directors"): directors = self.request()["directors"]
        else: directors = None
        if self.validate_field_not_null("release-dates"): release_dates = self.request()["release-dates"]
        else: release_dates = None
        if self.validate_field_not_null("synopsises"): synopsises = self.request()["synopsises"]
        else: synopsises = None
        if self.validate_field_not_null("genres"): genres = self.request()["genres"]
        else: genres = None
        
        query = Movie_Model.get_movie_model(filename, extension, path_on_disk, md5)
        if query is None:
            already_existed = False
            movie = Movie_Model.add_movie_model(original_title, duration, thumbnail_url, filename, extension, path_on_disk, md5)
            
    
class Create_Or_Get_Actor_WF(Base_Workflow):
    """
        INPUT:
            first_name
            last_name
            birth_date
            nick_name (optional)
            death_date (optional)
            awards (optional, list of Award_Model)
        OUTPUT:
            status = "ok"
            actor_id
            already_existed (boolean)
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
            first_name
            last_name
            birth_date
            nick_name (optional)
            death_date (optional)
            awards (optional, list of Award_Model)
        OUTPUT:
            status = "ok"
            writer_id
            already_existed (boolean)
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
            first_name
            last_name
            birth_date
            nick_name (optional)
            death_date (optional)
            awards (optional, list of Award_Model)
        OUTPUT:
            status = "ok"
            director_id
            already_existed (boolean)
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
            country_name
        OUTPUT:
            status = "ok"
            country_id
            already_existed (boolean)
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
            award_category_name
        OUTPUT:
            status = "ok"
            award_category_id
            already_existed (boolean)
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
            award_name
            date_of_awarding
            award_status (string, see Award_Model.STATUSES)
        RELATED INPUT:
            award_categories (list of Award_Category_Model)
        OUTPUT:
            status = "ok"
            award_id
            already_existed (boolean)
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
            genre_name
        OUTPUT:
            status = "ok"
            country_id
            already_existed (boolean)
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
            character_name
        RELATED INPUT:
            related_actors (list of Actor_Model)
            related_movies (list of Movie_Model)
        OUTPUT:
            status = "ok"
            country_id
            already_existed (boolean)
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