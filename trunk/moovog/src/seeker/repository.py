'''
Created on 30 avr. 2010

@author: Christophe
'''

from src.seeker.models import *

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
    def get_synopsis_model(country_model, movie_model):
        try:
            synopsis_model = Synopsis_Model.objects.get(country_model = country_model,
                                                        related_movie = movie_model)
        except Exception: return None
        return synopsis_model
    
    @staticmethod
    def get_genre_model(genre_name):
        try:
            genre_model = Genre_Model.objects.get(genre_name = genre_name)
        except Exception: return None
        return genre_model
    
    @staticmethod
    def get_release_date_model(country_model, movie_model):
        try:
            release_date_model = Release_Date_Model.objects.get(country_model = country_model,
                                                                related_movie = movie_model)
        except Exception: return None
        return release_date_model
    
    @staticmethod
    def add_awards(target_model, awards_models):
        if awards_models is not None:
            for award_model in awards_models:
                target_model.awards.add(award_model)
            target_model.save()
        return target_model
    
    @staticmethod
    def add_award_categories(target_model, award_category_models):
        if award_category_models is not None:
            for award_category_model in award_category_models:
                target_model.award_categories.add(award_category_model)
            target_model.save()
        return target_model