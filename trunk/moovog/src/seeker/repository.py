'''
Created on 30 avr. 2010

@author: Christophe
'''

from src.seeker.models import *
from tools.routines import areListEqual, special_dictionary_merger

class Repository:
    
    @staticmethod
    def get_synopsis_model(movie_model, country_models):
        """
            Searches for the movie's synopsis that is written in the same
            languages (countries).
            Returns that synopsis model if found, None if not.
        """
        country_names = []
        for country_model in country_models:
            country_names.append(country_model.country_name)
        
        movie_synopsis_models = movie_model.synopsis_model_set.all()
        
        for movie_synopsis_model in movie_synopsis_models:
            movie_synopsis_countries = movie_synopsis.countries.all()
            movie_synopsis_country_names = []
            for movie_synopsis_country in movie_synopsis_countries:
                movie_synopsis_country_names.append(movie_synopsis_country.country_name)
            if areListEqual(movie_synopsis_country_names, country_names):
                return movie_synopsis_model
        return None
    
    @staticmethod
    def get_release_date_model(movie_model, country_models):
        """
            Searches into the release dates of movie_model
            Tries to find a match between the countries of its release dates
            and the country_models
        """
        release_date_models = movie_model.release_data_model_set.all()
        for release_date_model in release_date_models:
            compared_list = release_date_model.countries.all()
            if len(country_models) == len(compared_list):
                # <beurk> ...
                country_names = []
                compared_names_list = []
                for country_model in country_models:
                    country_names.append(country_model.country_name)
                for compared_model in compared_list:
                    compared_names_list.append(compared_model.country_name)
                # <beurk /> ...
                if areListEqual(country_names, compared_names_list):
                    return release_date_model
        return None
    
    @staticmethod
    def add_awards(target_model, awards_models):
        for award_model in awards_models:
            target_model.awards.add(award_model)
        target_model.save()
        return target_model
    
    @staticmethod
    def add_award_categories(target_model, award_category_models):
        for award_category_model in award_category_models:
            target_model.award_categories.add(award_category_model)
        target_model.save()
        return target_model
    
    @staticmethod
    def add_countries(target_model, country_models):
        for country_model in country_models:
            target_model.countries.add(country_model)
        target_model.save()
        return target_model
    
    @staticmethod
    def search_all(string_to_search):
        """
            Calls all other repository search methods to find
            bindings between string_to_search and relevant
            content of each model
            
            OUTPUT :
                a merge of all other search methods OUTPUT
        """
        global_result = {}
        result = Repository().search_movie(string_to_search)
        global_result = special_dictionary_merger(result, global_result)
        result = Repository().search_actor(string_to_search)
        global_result = special_dictionary_merger(result, global_result)
        result = Repository().search_aka(string_to_search)
        global_result = special_dictionary_merger(result, global_result)
        result = Repository().search_award(string_to_search)
        global_result = special_dictionary_merger(result, global_result)
        result = Repository().search_character(string_to_search)
        global_result = special_dictionary_merger(result, global_result)
        result = Repository().search_director(string_to_search)
        global_result = special_dictionary_merger(result, global_result)
        result = Repository().search_genre(string_to_search)
        global_result = special_dictionary_merger(result, global_result)
        result = Repository().search_writer(string_to_search)
        global_result = special_dictionary_merger(result, global_result)
        return global_result
    
    @staticmethod
    def search_actor(string_to_search):
        """
            Searches into first_name and last_name of all
            Actor_Model instances
            
            OUTPUT :
                actor-models : a list of Actor_Model
        """
        query_first_name = Actor_Model.objects.filter(first_name__contains = string_to_search)
        query_last_name = Actor_Model.objects.filter(last_name__contains = string_to_search)
        result = []
        for model_id in query_first_name: result.append(Actor_Model.get_actor_model_by_id(model_id))
        for model_id in query_last_name: result.append(Actor_Model.get_actor_model_by_id(model_id))
        return {"actor-models" : result}
    
    @staticmethod
    def search_director(string_to_search):
        """
            Searches into first_name and last_name of all
            Director_Model instances
            
            OUTPUT :
                director-models : a list of Director_Model
        """
        query_first_name = Director_Model.objects.filter(first_name__contains = string_to_search)
        query_last_name = Director_Model.objects.filter(last_name__contains = string_to_search)
        result = []
        for model_id in query_first_name: result.append(Director_Model.get_director_model_by_id(model_id))
        for model_id in query_last_name: result.append(Director_Model.get_director_model_by_id(model_id))
        return {"director-models" : result}
    
    @staticmethod
    def search_writer(string_to_search):
        """
            Searches into first_name and last_name of all
            Writer_Model instances
            
            OUTPUT :
                writer-models : a list of Writer_Model
        """
        query_first_name = Writer_Model.objects.filter(first_name__contains = string_to_search)
        query_last_name = Writer_Model.objects.filter(last_name__contains = string_to_search)
        result = []
        for model_id in query_first_name: result.append(Writer_Model.get_writer_model_by_id(model_id))
        for model_id in query_last_name: result.append(Writer_Model.get_writer_model_by_id(model_id))
        return {"writer-models" : result}
    
    @staticmethod
    def search_movie(string_to_search):
        """
            Searches into original_title of all
            Movie_Model instances
            
            OUTPUT :
                movie-models : a list of Movie_Model
        """
        query = Movie_Model.objects.filter(original_title__contains = string_to_search)
        result = []
        for model_id in query: result.append(Movie_Model.get_movie_model_by_id(model_id))
        return {"movie-models" : result}
    
    @staticmethod
    def search_aka(string_to_search):
        """
            Searches into aka_name of all
            Aka_Model instances
            
            OUTPUT :
                movie-models : a list of Movie_Model
        """
        query = Aka_Model.objects.filter(aka_name__contains = string_to_search)
        result = []
        for model_id in query: result.append(Aka_Model.get_aka_model_by_id(model_id).related_movie)
        return {"movie-models" : result}
    
    @staticmethod
    def search_genre(string_to_search):
        """
            Searches into genre_name of all
            Genre_Model instances
            
            OUTPUT :
                movie-models : a list of Movie_Model
        """
        query = Genre_Model.objects.filter(genre_name__contains = string_to_search)
        result = []
        for model_id in query:
            for movie_model in Genre_Model.get_genre_model_by_id(model_id).movie_model_set.all():
                result.append(movie_model)
        return {"movie-models" : result}
    
    @staticmethod
    def search_character(string_to_search):
        """
            Searches into character_name of all
            Character_Model instances
            
            OUTPUT :
                movie-models : a list of Character_Model
                actor-models : a list of Actor_Model
        """
        query = Character_Model.objects.filter(character_name__contains = string_to_search)
        result_actors = []
        result_movies = []
        for model_id in query:
            character_model = Character_Model.get_character_model_by_id(model_id)
            result_actors.append(character_model.related_actor)
            result_movies.append(character_model.related_movie)
        return {"actor-models" : result_actors, "movie-models" : result_movies}
    
    @staticmethod
    def search_award(string_to_search):
        """
            Searches into award_name of all
            Award_Model instances
            
            OUTPUT :
                movie-models : a list of Movie_Model
                actor-models : a list of Actor_Model
                director-models : a list of Director_Model
                writer-models : a list of Writer_Model
        """
        query = Award_Model.objects.filter(award_name__contains = string_to_search)
        result_actors = []
        result_movies = []
        result_directors = []
        result_writers = []
        if query is not None:
            for model_id in query:
#                award_model = Award_Model.get_award_model_by_id(model_id)
                award_model = model_id
                movie_set = award_model.movie_model_set.all()
                actor_set = award_model.actor_model_set.all()
                director_set = award_model.director_model_set.all()
                writer_set = award_model.writer_model_set.all()
                if movie_set is not None:
                    for movie_model in movie_set:
                        result_movies.append(movie_model)
                if actor_set is not None:
                    for actor_model in actor_set:
                        result_actors.append(actor_model)
                if director_set is not None:
                    for director_model in director_set:
                        result_directors.append(director_model)
                if writer_set is not None:
                    for writer_model in writer_set:
                        result_writers.append(writer_model)
        return {"actor-models" : result_actors, "movie-models" : result_movies,
                "director-models" : result_directors, "writer-models" : result_writers}