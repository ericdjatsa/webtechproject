from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

import logging
import datetime

from src.seeker.workflows import *
from django.utils.simplejson import JSONDecoder, JSONEncoder

def index(request):
    return render_to_response("seeker/base.html", {})

def search(request):
    if request.method == "GET": HttpResponse("POST excepted")
    wf = Search_WF(request.POST, None)
    result = wf.work()
    return render_to_response("template_targeted", result)

def create_movie_completely(request):
    """
        This view requires of course a giant HTTP POST request to work.
        It's been gracefully written by Christophe (me ^^) to ease your
        efforts to feed seeker's models.
        Of course also, you can use a smoother method, which consist in
        building progressively the movie model, than the other models,
        then combine them together.
    
        INPUT :
            RELATED TO THE CURRENT MOVIE :
                original-title
                runtime
                user-rating
                thumbnail
                filename
                extension
                path
                md5
            RELATED TO COUNTRIES :
                original-country-names-list : [original-country-name-1, ...]
            RELATED TO AWARDS :
                awards : [{award-category-names-list : [award-category-name-1, ...], award-name,
                date-of-awarding, award-status}, ...]
            RELATED TO ACTORS :
                actors-list : [{first-name-1, last-name-1, birth-date-1, nick-name-1
                (None if None), death-date-1 (None if None), awards : {award-name-1 :
                award-category-name-1, ...}}, ...]
            RELATED TO CHARACTERS :
                characters-list : [{character-name-1, actor-first-name-1,
                actor-last-name-2}, ...]
            RELATED TO WRITERS :
                writers-list : [{first-name-1, last-name-1, birth-date-1, nick-name-1
                (None if None), death-date-1 (None if None), awards : {award-name-1 :
                award-category-name-1, ...}}, ...]
            RELATED TO DIRECTORS :
                directors-list : [{first-name-1, last-name-1, birth-date-1, nick-name-1
                (None if None), death-date-1 (None if None), awards : {award-name-1 :
                award-category-name-1, ...}}, ...]
            RELATED TO GENRES :
                genres-list : [genre-name] (list of genre names)
            RELATED TO AKAS :
                akas-list : {aka-name-1 : [country-name-1, country-names-2, ...], ...}
            RELATED TO RELEASE DATES :
                release-dates-list : {release-date-1 : [country-name-1, country-names-2, ...], ...}
            RELATED TO SYNOPSISES :
                synopsises-list : [[plain-text-1, country-name-1, country-names-2, ...], ...]
    """
    if request.method == "GET": HttpResponse("POST excepted")
    
    # Build or get the movie structure
    wf_start_movie = Create_Or_Get_Movie_WF(request.POST, None)
    result_start_movie = wf_start_movie.work()
    if result_start_movie["status"] == "ok":
        movie_model = result_start_movie["movie-model"]
    
    if not result_start_movie["already-existed"]:
        
        # Build or get the original countries of the movie
        original_country_models = []
        for original_country_name in request.POST["country-names-list"]:
            wf_create_original_country = Create_Or_Get_Country_WF({"country-name" : country_name}, None)
            result_create_original_country = wf_create_original_country.work()
            if result_create_original_country["status"] == "ok":
                original_country_models.append(result_create_original_country["country-model"])
        
        # Build or get the awards of the movie
        # Builds or get the award categories in the same step
        award_models = []
        for award_data in request.POST["awards"]:
            award_category_models = []
            for award_category_name in award_data["award-category-names-list"]:
                wf_create_award_category = Create_Or_Get_Award_Category_WF({"award-category-name" : award_category_name},
                                                                           None)
                result_create_award_category = wf_create_award_category.work()
                award_category_models.append(result_create_award_category["award-category"])
            wf_create_award = Create_Or_Get_Award_WF({"award-name" : award_data["award-name"],
                                                      "date-of-awarding" : award_data["date-of-awarding"],
                                                      "award-status" : award_data["award-status"],
                                                      "award-categories" : award_category_models},
                                                      None)
            result_create_award = wf_create_award.work()
            if result_create_award["status"] == "ok":
                award_models.append(result_create_award["award-model"])
        
        # Build or get the actors from the movie
        # Uses the previous award_models to get the matching actor_awards
        actor_models = []
        for actor_data in request.POST["actors-list"]:
            actor_awards = []
            for item in actor_data["awards"].iteritems():
                for award_model in award_models:
                    if item[0] == award_model.award_name:
                        award_category_models = award_model.award_categories.all()
                        for award_category_model in award_category_models:
                            if item[1] in award_category_model.award_category_name:
                                actor_awards.append(award_model)
            wf_create_actor = Create_Or_Get_Actor_WF({"first-name" : actor_data["first-name"],
                                                      "last-name" : actor_data["last-name"],
                                                      "birth-date" : actor_data["birth-date"],
                                                      "nick-name" : actor_data["nick-name"],
                                                      "death-date" : actor_data["death-date"],
                                                      "awards" : actor_awards},
                                                      None)
            result_create_actor = wf_create_actor.work()
            if result_create_actor["status"] == "ok":
                actor_models.append(result_create_actor["actor-model"])
        
        # Build or get the characters from the movie
        # Uses the previous actor_models to get the matching actor of the character
        character_models = []
        for character_data in request.POST["characters-list"]:
            for actor_model in actor_models:
                if (character_data["actor-first-name"] == actor_model.first_name and
                    character_data["actor-last-name"] == actor_model.last_name):
                    related_actor = actor_model
            wf_create_character = Create_Or_Get_Character_WF({"character-name" : character_data["character-name"],
                                                              "related-actor" : related_actor,
                                                              "related-movie" : movie_model},
                                                              None)
            result_create_character = wf_create_character.work()
            if result_create_character["status"] == "ok":
                character_models.append(result_create_character["character-model"])
        
        # Build or get the writers of the movie
        writer_models = []
        for writer_data in request.POST["writers-list"]:
            writer_awards = []
            for item in writer_data["awards"].iteritems():
                for award_model in award_models:
                    if item[0] == award_model.award_name:
                        award_category_models = award_model.award_categories.all()
                        for award_category_model in award_category_models:
                            if item[1] in award_category_model.award_category_name:
                                writer_awards.append(award_model)
            wf_create_writer = Create_Or_Get_Writer_WF({"first-name" : writer_data["first-name"],
                                                        "last-name" : writer_data["last-name"],
                                                        "birth-date" : writer_data["birth-date"],
                                                        "nick-name" : writer_data["nick-name"],
                                                        "death-date" : writer_data["death-date"],
                                                        "awards" : writer_awards},
                                                        None)
            result_create_writer = wf_create_writer.work()
            if result_create_writer["status"] == "ok":
                writer_models.append(result_create_writer["writer-model"])
        
        # Build or get the directors of the movie
        director_models = []
        for director_data in request.POST["directors-list"]:
            director_awards = []
            for item in director_data["awards"].iteritems():
                for award_model in award_models:
                    if item[0] == award_model.award_name:
                        award_category_models = award_model.award_categories.all()
                        for award_category_model in award_category_models:
                            if item[1] in award_category_model.award_category_name:
                                director_awards.append(award_model)
            wf_create_director = Create_Or_Get_Director_WF({"first-name" : director_data["first-name"],
                                                            "last-name" : director_data["last-name"],
                                                            "birth-date" : director_data["birth-date"],
                                                            "nick-name" : director_data["nick-name"],
                                                            "death-date" : director_data["death-date"],
                                                            "awards" : director_awards},
                                                            None)
            result_create_director = wf_create_director.work()
            if result_create_director["status"] == "ok":
                director_models.append(result_create_director["director-model"])
          
            
        # Build or get the genres of the movie
        genre_models = []
        for genre_name in request.POST["genres-list"]:
            wf_create_genre = Create_Or_Get_Genre_WF({"genre-name" : genre_name}, None)
            result_create_genre = wf_create_genre.work()
            if result_create_genre["status"] == "ok":
                genre_models.append(result_create_genre["genre-model"])
                
        # Build or get aka model for the movie
        # Builds or get the country models for the release dates
        aka_models = []
        for aka_data in request.POST["akas-list"].iteritems():
            aka_name = aka_data[0]
            aka_coutry_models = []
            for country_name in aka_data[1]:
                wf_create_country = Create_Or_Get_Country_WF({"country-name" : country_name}, None)
                result_create_country = wf_create_country.work()
                if result_create_country["status"] == "ok":
                    aka_coutry_models.append(result_create_country["country-model"])
            wf_create_aka = Create_Or_Get_Aka_WF({}, None)
            result_create_aka = wf_create_aka.work()
            if result_create_aka["status"] == "ok":
                aka_models.append(result_create_aka["aka-model"])
                
        # Build or get the release date of the movie
        # Builds or get the country models for the release dates
        release_date_models = []   
        for release_date_data in request.POST["release-dates-list"].iteritems():
            release_date = release_date_data[0]
            release_date_country_models = []
            for release_date_country_name in release_date_data[1]:
                wf_create_country = Create_Or_Get_Country_WF({"country-name" : release_date_country_name},
                                                             None)
                result_create_country = wf_create_country.work()
                if result_create_country["status"] == "ok":
                    release_date_country_models.append(result_create_country["country-model"])
            wf_create_release_date = Create_Or_Get_Release_Date_WF({"release-date" : release_date,
                                                                    "movie-model" : movie_model,
                                                                    "country-models" : release_date_country_models},
                                                                    None)
            result_create_release_date = wf_create_release_date.work()
            if result_create_release_date["status"] == "ok":
                release_date_models.append(result_create_release_date["release-date-model"])
        
        # Build or get the synopsises of the movie
        # Builds or get the country models for the synopsises
        synopsis_models = []
        # synopsises-list : [[plain-text-1, country-name-1, country-names-2, ...], ...]
        for synopsis_data in request.POST["synopsises-list"]:
            synopsis_plain_text = synopsis_data.pop(0)
            synposis_country_models = []
            for synopsis_country_name in synopsis_data:
                wf_create_country = Create_Or_Get_Country_WF({"country-name" : synopsis_country_name},
                                                             None)
                result_create_country = wf_create_country.work()
                if result_create_country["status"] == "ok":
                    synposis_country_models.append(result_create_country["country-model"])
            wf_create_synopsis = Create_Or_Get_Synopsises_WF({"plain-text" : synopsis_plain_text,
                                                              "movie-model" : movie_model,
                                                              "country-models" : synposis_country_models},
                                                             None)
            result_create_synopsis = wf_create_synopsis.work()
            if result_create_synopsis["status"] == "ok":
                synopsis_models.append(result_create_synopsis["synopsis-model"])
        
        # We finally complete the movie model
        wf_complete_movie = Complete_Movie_Model_WF({"movie-model" : movie_model,
                                                     "original-countries" : original_country_models,
                                                     "awards" : award_models,
                                                     "actors" : actor_models,
                                                     "writers" : writer_models,
                                                     "directors" : director_models,
                                                     "genres" : genre_models},
                                                     None)
        result_complete_movie = wf_complete_movie.work()
        
        if result_complete_movie["status"] == "ok":
            return render_to_response("template_targeted", {"movie-id" : movie_model.id})
    return HttpResponse("The movie you intended to create already existed")