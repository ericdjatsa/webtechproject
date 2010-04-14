from django.db import models
from base.Base_Models import Individual_Model

# Create your models here.

class Aka_Model(models.Model):
    aka = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    
    @classmethod
    def kind(cls):
        return "Aka_Model"
    
    @staticmethod
    def add_aka_model(aka_name, country):
        aka_model = Aka_Model()
        aka_model.aka = aka_name
        aka_model.country = country
        return aka_model

class Release_Date_Model(models.Model):
    release_date = models.DateField()
    country = models.CharField(max_length=100)
    
    @classmethod
    def kind(cls):
        return "Release_Date_Model"
    
    @staticmethod
    def add_release_date_model(date, country):
        release_date_model = Release_Date_Model()
        release_date_model.release_date = date
        release_date_model.country = country
        return release_date_model

class Synopsis_Model(models.Model):
    plain_text = models.TextField()
    country = models.CharField(max_length=100)
    
    @classmethod
    def kind(cls):
        return "Synopsis_Model"
    
    @staticmethod
    def add_synopsis_model(text, country):
        synopsis_model = Synopsis_Model()
        synopsis_model.plain_text = text
        synopsis_model.country = country
        return synopsis_model

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
    
class Movie_Model(models.Model):
    title = models.CharField(max_lentgh=200)
    akas = models.ManyToOneRel(Aka_Model)
    actors = models.ManyToOneRel(Actor_Model)
    writers = models.ManyToOneRel(Writer_Model)
    directors = models.ManyToOneRel(Director_Model)
    release_dates = models.ManyToOneRel(Release_Date_Model)
    synopsises = models.ManyToOneRel(Synopsis_Model)
    pass


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
        return "Movie_Model"

    @staticmethod
    def add_movie_model(titles, actors, writers, directors, release_date, synopsises, genres, duration,
                         identification_codes, trailers, crawled_date):
        movie = Movie_Model(titles = titles, actors = actors, writers = writers, directors = directors,
                              release_date = release_date, synopsises = synopsises, genres = genres,
                              duration = duration, identification_codes = identification_codes,
                              trailers = trailers, crawled_date = crawled_date)
        movie.is_data_fresh = True
        # serialize and put
        return movie