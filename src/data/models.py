'''
Created on 14 mars 2010

@author: Christophe
'''

from db.backends.mysql import creation
from base.Base_Models import Individual_Model
from base.Base_Models import WTP_Serializable_Model

class Moovie_Model(WTP_Serializable_Model):
    """ 
    titles : req, {[original], [akas]}
    actors : ref models {artist : character}
    writers : ref model
    directors / realisators : ref models
    release_dates : req, {en, fr, ...}
    synopsises : {en : ["synopsis1", "synopsis2", ...], fr : ["synopsis1", "synopsis2", ...], ...}
    genres : ["action", "drama", ...]
    duration : python time object
    identification_codes : {imdb : imdb_code, allocine : allocine_code, isbn : isbn_code, ...}
    trailers : {en : uri, fr : uri, ...}
    crawled_date : python datetime object
    is_data_fresh : True
    (next feature) is_data_valid : user evaluation
    """
    
    @classmethod
    def kind(cls):
        return "Moovie_Model"

    @staticmethod
    def add_moovie_model(titles, actors, writers, directors, release_date, synopsises, genres, duration,
                         identification_codes, trailers, crawled_date):
        moovie = Moovie_Model(titles = titles, actors = actors, writers = writers, directors = directors,
                              release_date = release_date, synopsises = synopsises, genres = genres,
                              duration = duration, identification_codes = identification_codes,
                              trailers = trailers, crawled_date = crawled_date)
        moovie.is_data_fresh = True
        # serialize and put
        return moovie

class Actor_Model(Individual_Model):
    
    @classmethod
    def kind(cls):
        return "Actor_Model"
    
    @staticmethod
    def add_actor_model(first_name, last_name, nick_name, birth_date, death_date, crawled_date, nominations):
        actor = Individual_Model.__init__(first_name, last_name, nick_name, birth_date, death_date, crawled_date)
        actor.nominations = nominations
        # serialize and put
        return actor

class Writer_Model(Individual_Model):
    
    @classmethod
    def kind(cls):
        return "Writer_Model"
    
    @staticmethod
    def add_writer_model(first_name, last_name, nick_name, birth_date, death_date, crawled_date, nominations):
        actor = Individual_Model.__init__(first_name, last_name, nick_name, birth_date, death_date, crawled_date)
        actor.nominations = nominations
        # serialize and put
        return actor
    
class Director_Model(Individual_Model):
    
    @classmethod
    def kind(cls):
        return "Director_Model"
    
    @staticmethod
    def add_director_model(first_name, last_name, nick_name, birth_date, death_date, crawled_date, nominations):
        actor = Individual_Model.__init__(first_name, last_name, nick_name, birth_date, death_date, crawled_date)
        actor.nominations = nominations
        # serialize and put
        return actor