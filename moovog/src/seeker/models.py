from django.db import models
from exceptions import NotImplementedError
from tools.routines import ModifyNoneToEmptyString

from django.utils import encoding, datetime_safe
        
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
    
    @staticmethod
    def get_or_create(self, nomination_name):
        nomination_model, created = Nomination_Model.objects.get_or_create(nomination_name = nomination_name)
        return nomination_model

#class Individual_Model(models.Model):
#    first_name = models.CharField(max_length=100)
#    last_name = models.CharField(max_length=100)
#    nick_name = models.CharField(max_length=100)
#    birth_date = models.DateField()
#    death_date = models.DateField()
#    nominations = models.ManyToManyField(Nomination_Model) # must be a list of NOMINATION_MODEL if any
#    
#    @classmethod
#    def kind(cls):
#        raise NotImplementedError
#    
#    def add_individual_model(first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
#        death_date = ModifyNoneToEmptyString(death_date)
#        nick_name = ModifyNoneToEmptyString(nick_name)
#        individual_model = Individual_Model(first_name = first_name, last_name = last_name, birth_date = birth_date,
#                                            nick_name = nick_name, death_date = death_date)            
#        individual_model.save()
#        for nomination in nominations:
#            individual_model.nominations.add(nomination)
#        individual_model.save()
#        return individual_model

class Actor_Model(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField()
    nominations = models.ManyToManyField(Nomination_Model) # must be a list of NOMINATION_MODEL if any
    
    @classmethod
    def kind(cls):
        return "Actor_Model"
    
#    def __init__(self, first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
#        death_date = ModifyNoneToEmptyString(death_date)
#        nick_name = ModifyNoneToEmptyString(nick_name)
#        actor_model = Individual_Model.__init__(self, first_name = first_name, last_name = last_name, birth_date = birth_date,
#                                                nick_name = nick_name, death_date = death_date)
#        for nomination in nominations:
#            individual_model.nominations.add(nomination)
#        actor_model.save()
#        return actor_model
#    
#    @staticmethod
#    def add_actor_model(first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
#        actor_model = Individual_Model.__init__(first_name, last_name, nick_name, birth_date, death_date, nominations)
#        actor_model.save()
#        for nomination in nominations:
#            individual_model.nominations.add(nomination)
#        actor_model.save()
#        return actor_model

    
    datetime_safe.real_date(1975,2,3)

    @staticmethod
    def get_or_create(first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
        death_date = ModifyNoneToEmptyString(death_date)
        nick_name = ModifyNoneToEmptyString(nick_name)
        actor_model, created = Actor_Model.objects.get_or_create(first_name = first_name,
                                                                 last_name = last_name,
                                                                 birth_date = birth_date,
                                                                 death_date = death_date,
                                                                 nick_name = nick_name)
        for nomination in nominations:
            individual_model.nominations.add(nomination)
        actor_model.save()
        return actor_model

class Writer_Model(models.Model):
    
    @classmethod
    def kind(cls):
        return "Writer_Model"
    
#    def __init__(self, first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
#        death_date = ModifyNoneToEmptyString(death_date)
#        nick_name = ModifyNoneToEmptyString(nick_name)
#        writer_model = Individual_Model.__init__(self, first_name = first_name, last_name = last_name, birth_date = birth_date,
#                                  nick_name = nick_name, death_date = death_date)
#        for nomination in nominations:
#            individual_model.nominations.add(nomination)
#        writer_model.save()
#        return writer_model
#
#    @staticmethod
#    def add_writer_model(first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
#        writer_model = Individual_Model.__init__(first_name, last_name, nick_name, birth_date, death_date)
#        writer_model.save()
#        for nomination in nominations:
#            individual_model.nominations.add(nomination)
#        writer_model.save()
#        return writer_model
    
class Director_Model(models.Model):
#    director = Director_Model.add_director_model("john", "doe", datetime.date.today())
#    from src.seeker.models import *
#    import datetime
    
    @classmethod
    def kind(cls):
        return "Director_Model"
    
#    def __init__(self, first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
#        death_date = ModifyNoneToEmptyString(death_date)
#        nick_name = ModifyNoneToEmptyString(nick_name)
#        Individual_Model.__init__(self, first_name = first_name, last_name = last_name, birth_date = birth_date,
#                                  nick_name = nick_name, death_date = death_date)
#    
#    @staticmethod
#    def add_director_model(first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
#        death_date = ModifyNoneToEmptyString(death_date)
#        nick_name = ModifyNoneToEmptyString(nick_name)
#        
#        director_model = Director_Model(first_name = first_name, last_name = last_name,
#                                        birth_date = birth_date, nick_name = nick_name,
#                                        death_date = death_date)
#        director_model.save()
#        
#        for nomination in nominations:
#            director_model.nominations.add(nomination)
#        director_model.save()
#        return director_model

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
    
    @staticmethod
    def get_or_create(self, country_name):
        country_model, created = Country_Model.objects.get_or_create(country_name = country_name)
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
    
    @staticmethod
    def get_or_create(self, aka_name, country_name):
        country_model = Country_Model.get_or_create(self, country_name)
        aka_model, created = Aka_Model.objects.get_or_create(aka_name = aka_name,
                                                             country = country_model)
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
    
    @staticmethod
    def get_or_create(self, release_date, country_name):
        country_model = Country_Model.get_or_create(self, country_name)
        release_date_model, created = Release_Date_Model.objects.get_or_create(release_date = release_date,
                                                                               country = country_model)
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
    
    @staticmethod
    def get_or_create(self, release_date, country_name):
        country_model = Country_Model.get_or_create(self, country_name)
        synopsis_model, created = Synopsis_Model.objects.get_or_create(plain_text = plain_text,
                                                                       country = country_model)
        return synopsis_model


    def get_type(self):
        return self.type
    
    @staticmethod
    def get_or_create(self, first_name, last_name, birth_date, death_date = None, nick_name = None, nominations = None):
        director_model, created = Director_Model.objects.get_or_create(first_name = first_name, last_name = last_name,
                                                               birth_date = birth_date, nick_name = nick_name,
                                                               death_date = death_date)
        for nomination in nominations:
            director_model.nominations.add(nomination)
        director_model.save()
        return director_model
    
class Genre_Model(models.Model):
    genre = models.CharField(max_length=100)
    
    @classmethod
    def kind(cls):
        return "Genre_Model"
    
    @staticmethod
    def add_genre_model(genre_name):
        genre_model = Genre_Model(genre = genre_name)
        genre_model.save()
        return genre_model
    
class Age_Restriction_Model(models.Model):
    age_restriction = models.IntegerField()
    country = models.ManyToManyField(Country_Model)
    
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
    
    thumbnail = models.CharField(max_length=255)
    filename = models.CharField(max_length=200)
    extension = models.CharField(max_length=32)
    path = models.CharField(max_length=200)
    md5 = models.CharField(max_length=32)
    
    @classmethod
    def kind(cls):
        return "Movie_Model"

    @staticmethod
    def add_movie_model(title, akas, actors, writers, directors, release_date, synopsises, genres, duration,
                        thumbnail_url, filename, extension, path_on_disk, md5):
        movie_model = Movie_Model(original_title = title,
                                  akas = akas,
                                  actors = actors,
                                  writers = writers,
                                  directors = directors,
                                  release_date = release_date,
                                  synopsises = synopsises,
                                  genres = genres,
                                  runtime = duration,
                                  thumbnail = thumbnail_url,
                                  filename = filename,
                                  extension = extension,
                                  path = path_on_disk,
                                  md5 = md5)
        movie_model.save()
        return movie_model