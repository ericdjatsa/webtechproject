from django.db import models

class Award_Category_Model(models.Model):
    award_category_name = models.CharField(max_length = 127) # Best Achievement in Visual Effects, ...
    
    @classmethod
    def kind(cls):
        return "Award_Category_Model"
    
    @staticmethod
    def add_award_category_model(award_category_name):
        award_category_model = Award_Category_Model(award_category_name = award_category_name)
        award_category_model.save()
        return award_category_model

    @staticmethod
    def get_award_category_model(award_category_name):
        try:
            query = Award_Category_Model.objects.filter(award_category_name = award_category_name)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_award_category_model_by_id(award_category_id):
        try:
            award_category_model = Award_Category_Model.objects.get(id = award_category_id)
        except Exception: return None
        return award_category_model
    
    @staticmethod
    def delete_award_category_model(award_category_id):
        award_category_model = Award_Category_Model.get_award_category_model_by_id(award_category_id)
        if award_category_model is None: return False
        else:
            award_category_model.delete()
            return True

class Award_Model(models.Model):
    award_name = models.CharField(max_length = 127) # Oscar, Saturn Award, Eddie ...
    date_of_awarding = models.DateField()
    award_categories = models.ManyToManyField(Award_Category_Model, through = "Award_Matcher_Model")
    award_status = models.CharField(max_length = 31)
    
    STATUSES = ["Won", "Nominated"]
    
    @classmethod
    def kind(cls):
        return "Award_Model"
    
    @staticmethod
    def add_award_model(award_name, date_of_awarding, award_status):
        if award_status not in Award_Model.STATUSES: award_status = None
        award_model = Award_Model(award_name = award_name, date_of_awarding = date_of_awarding,
                                  award_status = award_status)
        award_model.save()
        return award_model

    @staticmethod
    def get_award_model(award_name, date_of_awarding):
        try:
            query = Award_Model.objects.filter(award_name = award_name,
                                               date_of_awarding = date_of_awarding)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_award_model_by_id(award_id):
        try:
            award_model = Award_Model.objects.get(id = award_id)
        except Exception: return None
        return award_model
    
    @staticmethod
    def delete_award_model(award_id):
        award_model = Award_Model.get_country_model_by_id(award_id)
        if award_model is None: return False
        else:
            award_model.delete()
            return True
    
class Country_Model(models.Model):
    country_name = models.CharField(max_length = 127)
    
    @classmethod
    def kind(cls):
        return "Country_Model"
    
    @staticmethod
    def add_country_model(country_name):
        country_model = Country_Model(country_name = country_name)
        country_model.save()
        return country_model
    
    @staticmethod
    def get_country_model(country_name):
        try:
            query = Country_Model.objects.filter(country_name = country_name)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_country_model_by_id(country_id):
        try:
            country_model = Country_Model.objects.get(id = country_id)
        except Exception: return None
        return country_model
    
    @staticmethod
    def delete_country_model(country_id):
        country_model = Country_Model.get_country_model_by_id(country_id)
        if country_model is None: return False
        else:
            country_model.delete()
            return True
    
class Genre_Model(models.Model):
    genre_name = models.CharField(max_length = 127)
    
    @classmethod
    def kind(cls):
        return "Genre_Model"
    
    @staticmethod
    def add_genre_model(genre_name):
        genre_model = Genre_Model(genre_name = genre_name)
        genre_model.save()
        return genre_model
    
    @staticmethod
    def get_genre_model(genre_name):
        try:
            query = Genre_Model.objects.filter(genre_name = genre_name)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_genre_model_by_id(genre_id):
        try:
            genre_model = Genre_Model.objects.get(id = genre_id)
        except Exception: return None
        return genre_model
    
    @staticmethod
    def delete_genre_model(genre_id):
        genre_model = Genre_Model.get_genre_model_by_id(genre_id)
        if genre_model is None: return False
        else:
            genre_model.delete()
            return True
        
class Actor_Model(models.Model):
    first_name = models.CharField(max_length = 127)
    last_name = models.CharField(max_length = 127)
    nick_name = models.CharField(max_length = 127, null = True)
    birth_date = models.DateField()
    death_date = models.DateField(null = True)
    awards = models.ManyToManyField(Award_Model, through = "Award_Matcher_Model") # must be a list of Award_Model if any
    
    @classmethod
    def kind(cls):
        return "Actor_Model"
    
    @staticmethod
    def add_actor_model(first_name, last_name, birth_date, death_date = None, nick_name = None):
        actor_model = Actor_Model(first_name = first_name, last_name = last_name, nick_name = nick_name,
                                  birth_date = birth_date, death_date = death_date)
        actor_model.save()
        return actor_model

    @staticmethod
    def get_actor_model(first_name, last_name, birth_date):
        try:
            query = Actor_Model.objects.filter(first_name = first_name, last_name = last_name,
                                               birth_date = birth_date)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_actor_model_by_id(actor_id):
        try:
            actor_model = Actor_Model.objects.get(id = actor_id)
        except Exception: return None
        return actor_model
    
    @staticmethod
    def delete_actor_model(actor_id):
        actor_model = Actor_Model.get_actor_model_by_id(actor_id)
        if actor_model is None: return False
        else:
            actor_model.delete()
            return True

class Writer_Model(models.Model):
    first_name = models.CharField(max_length = 127)
    last_name = models.CharField(max_length = 127)
    nick_name = models.CharField(max_length = 127, null = True)
    birth_date = models.DateField()
    death_date = models.DateField(null = True)
    awards = models.ManyToManyField(Award_Model, through = "Award_Matcher_Model") # must be a list of Award_Model if any
    
    @classmethod
    def kind(cls):
        return "Writer_Model"
    
    @staticmethod
    def add_writer_model(first_name, last_name, birth_date, death_date = None, nick_name = None):
        writer_model = Writer_Model(first_name = first_name, last_name = last_name, nick_name = nick_name,
                                    birth_date = birth_date, death_date = death_date)
        writer_model.save()
        return writer_model

    @staticmethod
    def get_writer_model(first_name, last_name, birth_date):
        try:
            query = Writer_Model.objects.filter(first_name = first_name, last_name = last_name,
                                                birth_date = birth_date)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_writer_model_by_id(writer_id):
        try:
            writer_model = Writer_Model.objects.get(id = writer_id)
        except Exception: return None
        return writer_model
    
    @staticmethod
    def delete_writer_model(writer_id):
        writer_model = Writer_Model.get_writer_model_by_id(writer_id)
        if writer_model is None: return False
        else:
            writer_model.delete()
            return True
    
class Director_Model(models.Model):
    first_name = models.CharField(max_length = 127)
    last_name = models.CharField(max_length = 127)
    nick_name = models.CharField(max_length = 127, null = True)
    birth_date = models.DateField()
    death_date = models.DateField(null = True)
    awards = models.ManyToManyField(Award_Model, through = "Award_Matcher_Model") # must be a list of Award_Model if any
    
    @classmethod
    def kind(cls):
        return "Director_Model"
    
    @staticmethod
    def add_director_model(first_name, last_name, birth_date, death_date = None, nick_name = None, awards = None):
        director_model = Director_Model(first_name = first_name, last_name = last_name, nick_name = nick_name,
                                        birth_date = birth_date, death_date = death_date)
        director_model.save()
        return director_model

    @staticmethod
    def get_director_model(first_name, last_name, birth_date):
        try:
            query = Director_Model.objects.filter(first_name = first_name, last_name = last_name,
                                                  birth_date = birth_date)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_director_model_by_id(director_id):
        try:
            director_model = Director_Model.objects.get(id = director_id)
        except Exception: return None
        return director_model
    
    @staticmethod
    def delete_director_model(director_id):
        director_model = Director_Model.get_director_model_by_id(director_id)
        if director_model is None: return False
        else:
            director_model.delete()
            return True

class Movie_Model(models.Model):
    original_title = models.CharField(max_length = 255)
    # the original title of the movie, in original country(ies)
    original_countries = models.ManyToManyField(Country_Model)
    # the original movie country, from which it comes
    awards = models.ManyToManyField(Award_Model, through = "Award_Matcher_Model")
    # the awards of the movie (won or nominated, it has its importance)
    actors = models.ManyToManyField(Actor_Model)
    # actors of the movie
    writers = models.ManyToManyField(Writer_Model)
    # writers of the movie
    directors = models.ManyToManyField(Director_Model)
    # directors of the movie
    genres = models.ManyToManyField(Genre_Model)
    # action, thriller, love romance, ...
    runtime = models.TimeField()
    # time duration of the movie
    user_rating = models.FloatField()
    # user rating of the movie
    
    thumbnail_url = models.CharField(max_length=255)
    # url of the thumbnail of the movie
    filename = models.CharField(max_length=255)
    # name of movie on local disk
    extension = models.CharField(max_length=31)
    # .avi, .mkv, .mpeg, ...
    path = models.CharField(max_length=255)
    # path to movie on disk
    hash_code = models.CharField(max_length=31)
    # hashcode of the movie
    
    @classmethod
    def kind(cls):
        return "Movie_Model"

    @staticmethod
    def add_movie_model(original_title, duration, user_rating, thumbnail_url, filename, extension, path_on_disk, hash_code):
        movie_model = Movie_Model(original_title = original_title,
                                  runtime = duration,
                                  user_rating = user_rating,
                                  thumbnail_url = thumbnail_url,
                                  filename = filename,
                                  extension = extension,
                                  path = path_on_disk,
                                  hash_code = hash_code)
        movie_model.save()
        return movie_model
    
    @staticmethod
    def get_movie_model(filename, extension, path, hash_code):
        try:
            query = Movie_Model.objects.filter(filename = filename,extension = extension, path = path, hash_code = hash_code)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_movie_model_by_id(movie_id):
        try:
            movie_model = Movie_Model.objects.get(id = movie_id)
        except Exception: return None
        return movie_model
    
    @staticmethod
    def delete_movie_model(movie_id):
        movie_model = Movie_Model.get_movie_model_by_id(movie_id)
        if movie_model is None: return False
        else:
            movie_model.delete()
            return True
        
class Award_Matcher_Model(models.Model):
    movie = models.ForeignKey(Movie_Model)
    actor = models.ForeignKey(Actor_Model, null = True)
    director = models.ForeignKey(Director_Model, null = True)
    writer = models.ForeignKey(Writer_Model, null = True)
    award = models.ForeignKey(Award_Model)
    award_category = models.ForeignKey(Award_Category_Model)
    
    @classmethod
    def kind(cls):
        return "Award_Manager_Model"
    
    @staticmethod
    def add_award_matcher_model(movie, actor, director, writer, award, award_category):
        try:
            award_matcher_model = Award_Matcher_Model(movie = movie,
                                                      actor = actor,
                                                      director = director,
                                                      writer = writer,
                                                      award = award,
                                                      award_category = award_category)
            award_matcher_model.save()
        except Exception, x: return None
        return award_matcher_model
    
    @staticmethod
    def get_award_matcher(movie_model, actor_model, director_model, writer_model,
                          award_model, award_category_model):
        try:
            query = Award_Matcher_Model.objects.filter(movie = movie_model,
                                                               actor = actor_model,
                                                               director = director_model,
                                                               writer = writer_model,
                                                               award = award_model,
                                                               award_category = award_category_model)
        except Exception, x: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_award_matcher_by_id(award_matcher_id):
        try:
            award_matcher = Award_Matcher_Model.objects.get(id = award_matcher_id)
        except Exception, x: return None
        return award_matcher
    
    @staticmethod
    def delete_award_matcher_model(award_matcher_id):
        award_matcher = Award_Matcher_Model.get_award_matcher_by_id(award_matcher_id)
        if award_matcher is None: return False
        else:
            award_matcher.delete()
            return True
        
class Character_Model(models.Model):
    character_name = models.CharField(max_length = 127)
    related_actor = models.ForeignKey(Actor_Model)
    related_movie = models.ForeignKey(Movie_Model)
    
    @classmethod
    def kind(cls):
        return "Character_Model"
    
    @staticmethod
    def add_character_model(character_name, related_actor, related_movie):
        character_model = Character_Model(character_name = character_name, related_actor = related_actor,
                                          related_movie = related_movie)
        character_model.save()
        return character_model
    
    @staticmethod
    def get_character_model(character_name):
        try:
            query = Character_Model.objects.filter(character_name = character_name)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_character_model_by_id(character_id):
        try:
            character_model = Character_Model.objects.get(id = character_id)
        except Exception: return None
        return character_model
    
    @staticmethod
    def delete_character_model(character_id):
        character_model = Character_Model.get_character_model_by_id(character_id)
        if character_model is None: return False
        else:
            character_model.delete()
            return True

class Aka_Model(models.Model):
    aka_name = models.CharField(max_length = 127)
    countries = models.ManyToManyField(Country_Model)
    related_movie = models.ForeignKey(Movie_Model)
    
    @classmethod
    def kind(cls):
        return "Aka_Model"
    
    @staticmethod
    def add_aka_model(aka_name, movie_model):
        aka_model = Aka_Model(aka_name = aka_name, related_movie = movie_model)
        aka_model.save()
        return aka_model
    
    @staticmethod
    def get_aka_model(aka_name):
        try:
            query = Aka_Model.objects.filter(aka_name = aka_name)
        except Exception: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_aka_model_by_id(aka_id):
        try:
            aka_model = Aka_Model.objects.get(id = aka_id)
        except Exception: return None
        return aka_model
    
    @staticmethod
    def delete_aka_model(aka_id):
        aka_model = Aka_Model.get_aka_model_by_id(aka_id)
        if aka_model is None: return False
        else:
            aka_model.delete()
            return True

class Release_Date_Model(models.Model):
    release_date = models.DateField()
    countries = models.ManyToManyField(Country_Model)
    related_movie = models.ForeignKey(Movie_Model)
    
    @classmethod
    def kind(cls):
        return "Release_Date_Model"
        
    @staticmethod
    def add_release_date_model(release_date, related_movie_model):
        release_date_model = Release_Date_Model(release_date = release_date,
                                                related_movie = related_movie_model)
        release_date_model.save()
        return release_date_model
    
    @staticmethod
    def get_release_date_model(release_date, related_movie):
        try:
            query = Release_Date_Model.objects.filter(release_date = release_date,
                                                      related_movie = related_movie)
        except Exception, x: return None
        if len(query) != 0: return query[0]
        else: return None
    
    @staticmethod
    def get_release_date_model_by_id(release_date_id):
        try:
            release_date_model = Release_Date_Model.objects.get(id = release_date_id)
        except Exception: return None
        return release_date_model
    
    @staticmethod
    def delete_release_date_model(release_date_id):
        release_date_model = Release_Date_Model.get_release_date_model_by_id(release_date_id)
        if release_date_model is None: return False
        else:
            release_date_model.delete()
            return True

class Synopsis_Model(models.Model):
    plain_text = models.TextField()
    countries = models.ManyToManyField(Country_Model)
    related_movie = models.ForeignKey(Movie_Model)
    
    @staticmethod
    def add_synopsis_model(plain_text, related_movie_model):
        synopsis_model = Synopsis_Model(plain_text = plain_text,
                                        related_movie = related_movie_model)
        synopsis_model.save()
        return synopsis_model
    
    @staticmethod
    def get_synopsis_model_by_id(synopsis_id):
        try:
            synopsis_model = Synopsis_Model.objects.get(id = synopsis_id)
        except Exception: return None
        return synopsis_model
    
    @staticmethod
    def delete_synopsis_model(synopsis_id):
        synopsis_model = Synopsis_Model.get_synopsis_model_by_id(synopsis_id)
        if synopsis_model is None: return False
        else:
            synopsis_model.delete()
            return True