'''
Created on 30 avr. 2010

@author: Christophe
'''

from src.seeker.models import *
from tools.routines import areListEqual

class Repository:
    
    @staticmethod
    def get_movie_model_by_original_title_and_release_date(original_title, release_date):
        try:
            genre_model = Movie_Model.objects.get(genre_name = genre_name)
        except Exception: return None
        return genre_model
    
    @staticmethod
    def get_movie_model_by_aka_and_release_year(aka, release_date):
        try:
            genre_model = Movie_Model.objects.get(genre_name = genre_name)
        except Exception: return None
        return genre_model
    
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