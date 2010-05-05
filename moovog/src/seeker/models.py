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
            award_category_model = Award_Category_Model.objects.get(award_category_name = award_category_name)
        except Exception: return None
        return award_category_model
    
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
    award_categories = models.ManyToManyField(Award_Category_Model)
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
            award_model = Award_Model.objects.get(award_name = award_name,
                                                  date_of_awarding = date_of_awarding)
        except Exception: return None
        return award_model
    
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
            country_model = Country_Model.objects.get(country_name = country_name)
        except Exception: return None
        return country_model
    
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
            genre_model = Genre_Model.objects.get(genre_name = genre_name)
        except Exception: return None
        return genre_model
    
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
    awards = models.ManyToManyField(Award_Model) # must be a list of Award_Model if any
    
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
            actor_model = Actor_Model.objects.get(first_name = first_name, last_name = last_name,
                                                  birth_date = birth_date)
        except Exception: return None
        return actor_model
    
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
    awards = models.ManyToManyField(Award_Model) # must be a list of Award_Model if any
    
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
            writer_model = Writer_Model.objects.get(first_name = first_name, last_name = last_name,
                                                    birth_date = birth_date)
        except Exception: return None
        return writer_model
    
    @staticmethod
    def get_writer_model_by_id(actor_id):
        try:
            writer_model = Writer_Model.objects.get(id = actor_id)
        except Exception: return None
        return writer_model
    
    @staticmethod
    def delete_writer_model(actor_id):
        writer_model = Writer_Model.get_writer_model_by_id(actor_id)
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
    awards = models.ManyToManyField(Award_Model) # must be a list of Award_Model if any
    
    @classmethod
    def kind(cls):
        return "Director_Model"
    
    def add_awards(self, awards_models):
        if awards_models is not None:
            for award_model in awards_models:
                self.awards.add(award_model)
            self.save()
        return self
    
    @staticmethod
    def add_writer_model(first_name, last_name, birth_date, death_date = None, nick_name = None, awards = None):
        director_model = Director_Model(first_name = first_name, last_name = last_name, nick_name = nick_name,
                                        birth_date = birth_date, death_date = death_date)
        director_model.save()
        return director_model.add_awards(awards)

    @staticmethod
    def get_director_model(first_name, last_name, birth_date):
        try:
            director_model = Director_Model.objects.get(first_name = first_name, last_name = last_name,
                                                        birth_date = birth_date)
        except Exception: return None
        return director_model
    
    @staticmethod
    def get_director_model_by_id(actor_id):
        try:
            director_model = Director_Model.objects.get(id = actor_id)
        except Exception: return None
        return director_model
    
    @staticmethod
    def delete_director_model(actor_id):
        director_model = Director_Model.get_director_model_by_id(actor_id)
        if director_model is None: return False
        else:
            director_model.delete()
            return True

class Movie_Model(models.Model):
    original_title = models.CharField(max_length = 255)
    # the original title of the movie, in original country(ies)
    original_countries = models.ManyToManyField(Country_Model)
    # the original movie country, from which it comes
    awards = models.ManyToManyField(Award_Model)
    # the differents "as known as" titles, with related country(ies)
    # SHOULDN'T BE this way, in a perfect design
    # We should have a Foreign key to Movie_Model in Award_Model
    # We can't have that, thanks to django linear parsing of models.py file
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
    filename = models.CharField(max_length=200)
    # name of movie on local disk
    extension = models.CharField(max_length=32)
    # .avi, .mkv, .mpeg, ...
    path = models.CharField(max_length=200)
    # path to movie on disk
    hash_code = models.CharField(max_length=32)
    # md5 of the movie (1st minute)
    
    @classmethod
    def kind(cls):
        return "Movie_Model"

    @staticmethod
    def add_movie_model(original_title, duration, user_rating, thumbnail_url, filename, extension, path_on_disk, hashcode):
        movie_model = Movie_Model(original_title = original_title,
                                  runtime = duration,
                                  user_rating = user_rating,
                                  thumbnail_url = thumbnail_url,
                                  filename = filename,
                                  extension = extension,
                                  path = path_on_disk,
                                  hash_code = hashcode)
        movie_model.save()
        return movie_model
    
    @staticmethod
    def get_movie_model(filename, extension, path, md5):
        try:
            movie_model = Movie_Model.objects.get(filename = filename, extension = extension,
                                                  path = path, md5 = md5)
        except Exception: return None
        return movie_model
    
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
        
class Character_Model(models.Model):
    character_name = models.CharField(max_length = 127)
    related_actors = models.ForeignKey(Actor_Model)
    related_movies = models.ForeignKey(Movie_Model)
    
    @classmethod
    def kind(cls):
        return "Character_Model"
    
    @staticmethod
    def add_character_model(character_name, related_actors, related_movies):
        character_model = Character_Model(character_name = character_name, related_actors = related_actors,
                                          related_movies = related_movies)
        character_model.save()
        return character_model
    
    @staticmethod
    def get_character_model(character_name):
        try:
            character_model = Character_Model.objects.get(character_name)
        except Exception: return None
        return character_model
    
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
    
    def add_countries(self, country_models):
        # countries is a list of Country_Model
        if country_models is not None:
            for country_model in country_models:
                self.countries.add(country_model)
            self.save()
        return self
    
    @staticmethod
    def add_aka_model(aka_name, countries, movie_model):
        aka_model = Aka_Model(aka_name = aka_name, related_movie = movie_model)
        aka_model.save()
        return aka_model.add_country(countries)
    
    @staticmethod
    def get_aka_model(aka_name):
        try:
            aka_model = Aka_Model.objects.get(aka_name = aka_name)
        except Exception: return None
        return aka_model
    
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
    country = models.ManyToManyField(Country_Model)
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