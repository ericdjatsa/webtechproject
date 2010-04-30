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
    
class Find_Movie_By_Actor(Base_Workflow):
    pass

class Find_Actor(Base_Workflow):
    pass

class Find_Director(Base_Workflow):
    pass

class Find_Writer(Base_Workflow):
    pass

class Fake_Actor_Builder(Base_Workflow):
    '''    FAKER TO BUILD ACTORS
        INPUT :
            first_name
            last_name
            birth_date
            nick_name (optional)
            death_date (optional)
            nominations (optional) : [nomination1, nomination2, ...]
        OUTPUT :
            status : "ok"
            actor model id
    '''    
    def __init__(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
        
    def validate_input(self):
        self.validate_string_field_not_empty("first-name")
        self.validate_string_field_not_empty("last-name")
        self.validate_date_field("birth-date")
        
    def process(self):
        first_name = self.request()["first-name"]
        last_name = self.request()["last-name"]
        birth_date = self.request()["birth-date"]
        if self.request()["death-date"] is not None: death_date = self.request()["death-date"]
        else: death_date = None
        if self.request()["nick-name"] is not None: nick_name = self.request()["nick-name"]
        else: nick_name = None
        if self.request()["nominations"] is not None: nominations = self.request()["nominations"]
        else: nominations = None
        
        try:
            actor_model = Actor_Model.add_actor_model(first_name, last_name, birth_date, death_date, nick_name, nominations)
        except Exception, x: logging.error("failed to add fake actor")
        
        self.add_to_response("status", "ok")
        self.add_to_response("actor-id", actor_model.id)

class Fake_Movie_Builder(Base_Workflow):
    '''    FAKER TO BUILD MOVIES
        INPUT :
            original_title
            akas : [{en : en_aka, fr : fr_aka, ...}]
            actors : [actor1, actor2]
            writers
            directors
            release_dates
            synopsises
            genres
            runtime
        OUTPUT :
            status : "ok"
            movie model id
    '''    
    def __init(self, input, authorization):
        Base_Workflow.__init__(self, input, authorization_pipe)
    
    def validate_input(self):
        self.validate_string_field_not_empty("original-title")
        self.validate_string_field_not_empty("aka")
        pass
    
    def process(self):
        pass