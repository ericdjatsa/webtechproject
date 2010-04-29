from django.db import models
from base.Base_Models import Individual_Model



class Country_Model(models.Model):
    country_name = models.CharField(max_length=100)
    
    @classmethod
    def kind(cls):
        return "Country_Model"
    
    @staticmethod
    def add_aka_model(aka_name, country):
        country_model = Country_Model(country_name = country)
        country_model.save()
        return country_model
    
class Aka_Model(models.Model):
    aka_name = models.CharField(max_length=100)
    country = models.ManyToManyField(Country_Model)
    
    @classmethod
    def kind(cls):
        return "Aka_Model"
    
    @staticmethod
    def add_aka_model(aka, country):
        aka_model = Aka_Model(aka_name = aka, country = country)
        aka_model.save()
        return aka_model

class Release_Date_Model(models.Model):
    release_date = models.DateField()
    country = models.ManyToManyField(Country_Model)
    
    @classmethod
    def kind(cls):
        return "Release_Date_Model"
    
    @staticmethod
    def add_release_date_model(date, country):
        release_date_model = Release_Date_Model(release_date = date, country = country)
        release_date_model.save()
        return release_date_model

class Synopsis_Model(models.Model):
    plain_text = models.TextField()
    country = models.ManyToManyField(Country_Model)
    
    @classmethod
    def kind(cls):
        return "Synopsis_Model"
    
    @staticmethod
    def add_synopsis_model(text, country):
        synopsis_model = Synopsis_Model(plain_text = text, country = country)
        synopsis_model.save()
        return synopsis_model

class Actor_Model(Individual_Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField()
    nominations = models.ManyToManyField(Nomination_Model)
    
    @classmethod
    def kind(cls):
        return "Actor_Model"
    
    @staticmethod
    def add_actor_model(first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
        actor_model = Individual_Model.__init__(first_name, last_name, nick_name, birth_date, death_date, nominations)
        actor_model.save()
        return actor_model

class Writer_Model(Individual_Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField()
    nominations = models.ManyToManyField(Nomination_Model)
    
    @classmethod
    def kind(cls):
        return "Writer_Model"
    
    @staticmethod
    def add_writer_model(first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
        writer_model = Individual_Model.__init__(first_name, last_name, nick_name, birth_date, death_date, nominations)
        writer_model.save()
        return writer_model
    
class Director_Model(Individual_Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField()
    nominations = models.ManyToOneRel(Nomination_Model)
    
    @classmethod
    def kind(cls):
        return "Director_Model"
    
    @staticmethod
    def add_director_model(first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
        director_model = Individual_Model.__init__(first_name, last_name, nick_name, birth_date, death_date, nominations)
        director_model.save()
        return director_model
    
class Genre_Model(models.Model):
    genre = models.ManyToManyField(Movie_Model)
    
    @classmethod
    def kind(cls):
        return "Genre_Model"
    
    @staticmethod
    def add_genre_model(genre_name):
        genre_model = Genre_Model(genre = genre_name)
        genre_model.save()
        return genre_model

class Nomination_Model(models.Model):
    nomination_name = models.CharField(max_length=100)
    nomination_year = models.DateField()
    
    @classmethod
    def kind(cls):
        return "Nomination_Model"
    
    @staticmethod
    def add_nomination_model(name, year):
        nomination_model = Nomination_Model(nomination_name = name, nomination_year = year)
        nomination_model.save()
        return nomination_model
    
class Age_Restriction_Model(models.Model):
    age_restriction = models.CharField(max_length=20)
    country = models.ManyToManyField()
    
    @classmethod
    def kind(cls):
        return "Age_Restriction_Model"
    
    @staticmethod
    def add_nomination_model(age, country):
        age_restriction_model = Age_Restriction_Model(age_restriction = age, country = country)
        age_restriction_model.save()
        return age_restriction_model

class Movie_Model(models.Model):
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
    """
    original_title = models.CharField(max_length=100)
    akas = models.ManyToManyField(Aka_Model)
    actors = models.ManyToManyField(Actor_Model)
    writers = models.ManyToManyField(Writer_Model)
    directors = models.ManyToManyField(Director_Model)
    release_dates = models.ManyToManyField(Release_Date_Model)
    synopsises = models.ManyToManyField(Synopsis_Model)
    genres = models.ManyToManyField(Genre_Model)
    runtime = models.TimeField()
    
    @classmethod
    def kind(cls):
        return "Movie_Model"

    @staticmethod
    def add_movie_model(title, akas, actors, writers, directors, release_date, synopsises, genres, duration):
        movie_model = Movie_Model(original_title = title,
                                  akas = akas,
                                  actors = actors,
                                  writers = writers,
                                  directors = directors,
                                  release_date = release_date,
                                  synopsises = synopsises,
                                  genres = genres,
                                  runtime = duration)
        movie_model.save()
        return movie_model