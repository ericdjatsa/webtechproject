# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2010

@author: Christophe
'''

try:
    from src.seeker.models import *
except Exception, x: from seeker.models import *
from tools.routines import areListEqual, homogeneous_search_dictionary_merger, heterogeneous_search_dictionary_merger
#try:
#    from src.seeker import ranking_methods
#except Exception, x: from seeker import ranking_methods

class Repository:

    @staticmethod
    def get_release_date_model(movie_model, country_models):
        """
            Searches into the release dates of movie_model
            Tries to find a match between the countries of its release dates
            and the country_models
        """
        release_date_models = movie_model.release_date_model_set.all()
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
    def get_movies_by_freshness(number_of_result = 0):
        if number_of_result > 0:
            return Movie_Model.objects.order_by("first_created")[:number_of_result]
    
    @staticmethod
    def get_last_modified_movies(number_of_result = 0):
        if number_of_result > 0:
            return Movie_Model.objects.order_by("last_modified")[:number_of_result]
    
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
        global_result = homogeneous_search_dictionary_merger(result, global_result)
        result = Repository().search_actor(string_to_search)
        global_result = homogeneous_search_dictionary_merger(result, global_result)
        result = Repository().search_aka(string_to_search)
        global_result = homogeneous_search_dictionary_merger(result, global_result)
        result = Repository().search_director(string_to_search)
        global_result = homogeneous_search_dictionary_merger(result, global_result)
        result = Repository().search_genre(string_to_search)
        global_result = homogeneous_search_dictionary_merger(result, global_result)
        result = Repository().search_writer(string_to_search)
        global_result = homogeneous_search_dictionary_merger(result, global_result)
        result = Repository().search_award(string_to_search)
#        global_result = heterogeneous_search_dictionary_merger(result, global_result)
#        result = Repository().search_character(string_to_search)
#        global_result = heterogeneous_search_dictionary_merger(result, global_result)
#        result = Repository().search_award_category(string_to_search)
#        global_result = heterogeneous_search_dictionary_merger(result, global_result)
        return global_result
    
    @staticmethod
    def search_actor(string_to_search):
        """
            Searches into full_name of all Actor_Model instances
            
            OUTPUT :
                actor-models : a list of Actor_Model
        """
        query = Actor_Model.objects.filter(full_name__icontains = string_to_search)
        result = []
        for model in query: result.append(model)
        return {"actor-models" : result}
    
    @staticmethod
    def search_director(string_to_search):
        """
            Searches into full_name of all Director_Model instances
            
            OUTPUT :
                director-models : a list of Director_Model
        """
        query = Director_Model.objects.filter(full_name__icontains = string_to_search)
        result = []
        for model in query: result.append(model)
        return {"director-models" : result}
    
    @staticmethod
    def search_writer(string_to_search):
        """
            Searches into full_name of all Writer_Model instances
            
            OUTPUT :
                writer-models : a list of Writer_Model
        """
        query = Writer_Model.objects.filter(full_name__icontains = string_to_search)
        result = []
        for model in query: result.append(model)
        return {"writer-models" : result}
    
    @staticmethod
    def search_movie(string_to_search):
        """
            Searches into original_title of all
            Movie_Model instances
            
            OUTPUT :
                movie-models : a list of Movie_Model
        """
        query = Movie_Model.objects.filter(original_title__icontains = string_to_search)
        result = []
        for model in query: result.append(model)
        return {"movie-models" : result}
    
    @staticmethod
    def search_aka(string_to_search):
        """
            Searches into aka_name of all
            Aka_Model instances
            
            OUTPUT :
                movie-models : a list of Movie_Model
        """
        query = Aka_Model.objects.filter(aka_name__icontains = string_to_search)
        result = []
        for model in query: result.append(model)
        return {"movie-models" : result}
    
    @staticmethod
    def search_genre(string_to_search):
        """
            Searches into genre_name of all
            Genre_Model instances
            
            OUTPUT :
                movie-models : a list of Movie_Model
        """
        query = Genre_Model.objects.filter(genre_name__icontains = string_to_search)
        result = []
        for genre_model in query:
            for movie_model in genre_model.movie_model_set.all():
                result.append(movie_model)
        return {"movie-models" : result}
    
    @staticmethod
    def search_character(string_to_search):
        """
            Searches into character_name of all
            Character_Model instances
            
            OUTPUT :
                {match-1 : {"actor" : actor_1, "movie" : movie_1}, match-2 : ...}
        """
        query = Character_Model.objects.filter(character_name__icontains = string_to_search)
        result = {}
        i = 0
        if query is not None:
            for character_model in query:
                i += 1
                result["match"+str(i)] = {}
                result["match"+str(i)]["actor"] = character_model.related_actor
                result["match"+str(i)]["movie"] = character_model.related_movie
        return result
    
    @staticmethod
    def search_award(string_to_search):
        """
            Searches into award_name of all
            Award_Model instances
            
            OUTPUT :
                {match-1 : {"movie" : movie_1, "person" : person_1, "award-category" : 
                award_category_1, "date-of-awarding" : date, award-status : status
                }, match-2 : ...}
        """
        query = Award_Model.objects.filter(award_name__icontains = string_to_search)
        result = {}
        if query is not None:
            for award_model in query:
                matches = Award_Matcher_Model.objects.filter(award = award_model)
                i = 0
                if matches is not None:
                    for match in matches:
                        i += 1
                        result["match"+str(i)] = {}
                        result["match"+str(i)]["movie"] = match.movie
                        if match.actor is not None: result["match"+str(i)]["person"] = match.actor
                        elif match.director is not None: result["match"+str(i)]["person"] = match.director
                        elif match.writer is not None: result["match"+str(i)]["person"] = match.writer
                        else: result["match"+str(i)]["person"] = None
                        result["match"+str(i)]["award-category"] = match.award_category
                        result["match"+str(i)]["date-of-awarding"] = award_model.date_of_awarding
                        result["match"+str(i)]["award-status"] = award_model.award_status
        return result

    @staticmethod
    def search_award_category(string_to_search):
        """
            Searches into award_category_name of all
            Award_Category_Model instances
            
            OUTPUT :
                models : {"movie_model" : [actor_model_1, ...], ...}
        """
        query = Award_Category_Model.objects.filter(award_category_name__icontains = string_to_search)
        result = {}
        for award_category_model in query:
            matcher_list = award_category_model.award_matcher_model_set.all()
            if matcher_list is not None:
                i = 0
                for award_matcher_model in matcher_list:
                    i += 1
                    result["award-category-"+str(i)] = []
                    result["award-category-"+str(i)].append(award_matcher_model.actor)
                    result["award-category-"+str(i)].append(award_matcher_model.director)
                    result["award-category-"+str(i)].append(award_matcher_model.writer)
                    result["award-category-"+str(i)].append(award_matcher_model.movie)
                    result["award-category-"+str(i)].append(award_matcher_model.award)
                    result["award-category-"+str(i)].append(award_matcher_model.award_category)
        return result
    
    @staticmethod    
    def get_attr_value(model_object,attribute_name):
        from operator import attrgetter #We need this to get an attribute's value given it's name
        
        attribute_value=''
        try :
            attribute_value=map(attrgetter(attribute_name),[model_object])[0] #gets the value of the attribute correspondent to attribute_name
        except AttributeError:
            
            #If this exception is raised it means the attribute name does not exist for that model,it therefore means that the attribute name is a fictitious attribute for the Movie model created on purpose in the ranking method
            
            #I go through the dictionary of akas in the Movie model and I retrieve the correspondent akas_value
           
            attribute_value=model_object.infos["akas"].get(attribute_name)
            
        return attribute_value
        
    @staticmethod   
    def basic_rank(model_object,attribute_name,search_word,weights):
        '''
        This function perform a basic ranking based on a single word input and works on string attributes of the model
    
        INPUT :
                model_object, attribute name,search_word,weights dictionnary
        OUTPUT :
                rank_value : the rank of the correspondent model according to the searched word
        '''
        
        tmp_rank=0
        attribute_value=Repository.get_attr_value(model_object,attribute_name)#gets the value of the attribute correspondent to attribute_name
        
        rank_value=0 #each time I have to rank an object I re-initialise its rank to 0
    
        #first I check if the search string is contained in the attribute_value
        
        if search_word in attribute_value.lower() :
            tmp_rank+=weights[attribute_name]*(float(len(search_word))/len(attribute_value)) #I multiply by a factor that takes into consideration the length of the search_word
    
        #Then I compute the number of occurences of search_string
        tmp_rank+=attribute_value.lower().count(search_word)
        #the risk with this computation is that if the users enters "th" as search string it is likely that "th" occurs many times in a movie title,but this is not really a problem at the end
    
        #finally I check the position of the search string in the ref_attribute
        index=attribute_value.lower().find(search_word)
    
        if index != -1 :
            tmp_rank+=((len(attribute_value) - index)/float(len(attribute_value)))*weights[attribute_name]
        # the float function inserted above is a trick to let python to consider the operands as float numbers rather than integers
        return tmp_rank
        
    @staticmethod    
    def compute_rank(model_object,attributes,search_string,weights): #Not for Movie Model !
        '''
        This function perform a more complex ranking based on a string input by spliting the string into single words and combining the ranks computed for each word
        N.B: This function is not usable for Movie Models it works only for Actor,Director,Writer... 
    
        INPUT :
                model_type,model_object,attributes(on which to perform the ranking),search_string,weights
        OUTPUT :
                rank_value : the rank of the correspondent model according to the searched string
        '''
        
        tmp_rank=0
        search_string=search_string.lower()#I turn the string into lower case
        #I split the search_string into words
        words=search_string.split()
        #I transform words in a Set of unique words i.e ['the', 'man', 'gives', 'the', 'other', 'man', 'the', 'book'] becomes ['the','man','gives','other','book'] this is to avoid computing the basic_rank more than ones for the same word
        s=set(words)#this is a Set of unique words
        words=list(s) #I recover a list
    
        if len(words) > 1 :
            #If the string is composed of more than one word I first perform the rank considering the entire search_string
            for attr in attributes :
                tmp_rank+=Repository.basic_rank(model_object,attr,search_string,weights)   
    
        #Now I compute seperate ranks
        for w in words:
            w_index=search_string.find(w) #it can't return -1 ^_^ so I can avoid the check
            for attr in attributes :
                tmp_rank+=Repository.basic_rank(model_object,attr,w,weights)*((len(search_string) - w_index)/float(len(search_string)))
    
            #the following computation has to be reviewed[could be optional because the scenario in which it really applies occurs seldom]
            occurs=search_string.count(w) #I compute the occurences of w in the search string,remember the case in which the user enters like search_string: 'Le fabuleux le ' we should take into account the fact that he entered twice the word 'le'
            tmp_rank+=float((occurs-1))/len(search_string) #I substract 1 so that in case the occurence is equal to 1, I don't increase the rank
        return tmp_rank
    
    @staticmethod    
    def rank(models_type,models_list,search_string):
        '''
        This function perform the ranking of several models object passed as input based on the search string
        INPUT :
               models type(Actor,Movie,etc...),list of models to rank(models_list), search_string
        OUTPUT :
                list of models ranked by decreasing rank_value
        '''
        if models_type in ['Actor_Model','Director_Model','Writer_Model'] :
            WEIGHTS = {u"full_name" : 5,u"nick_name":3}
        elif models_type=='Movie_Model' :
            WEIGHTS = {u"original_title" : 5}
        elif models_type=='Award_Model' :
            WEIGHTS = {u"award_name" : 5}
    
        
        attributes=list(WEIGHTS)
        
        mods={} #dictionnary key=models_str_representation value=models rank_value
        sorted_models=[]
        
        for mod in models_list :
            
            rnk=Repository.compute_rank(mod,attributes,search_string,WEIGHTS) #this is the first computation of the rank    
            
            
            if models_type=='Movie_Model':
				#Taking into account the user rating could provide a wrong ranking to the models because a movie can we very well rated by the users but be irelevant for the search_string
				#To solve this issue,I assign to the movie's original_title attribute a very high weight with respect to the user rating weight
                WEIGHTS["user_rating"]=1
                rnk+=float(mod.user_rating)*WEIGHTS["user_rating"]
            elif models_type=='Award_Model' :       
                #update rnk based on number of connections to the award
                WEIGHTS["award_categories"]=0.5
                rnk+=len(mod.award_categories)*WEIGHTS["award_categories"]
                
            mods[str(mod)]=rnk
        
        #print '\n\nmods dictionnary',mods
        
        sorted_models=sorted(models_list,key=lambda mod:mods.get(str(mod)),reverse=True)
        return sorted_models #returns a list of sorted models according to decreasing rank
