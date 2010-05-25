# -*- coding: utf-8 -*-
from django.db import models
from operator import attrgetter #We need this to get an attribute's value given it's name


class Award_Category_Model(models.Model):
    award_category_name = models.CharField(max_length = 127) # Best Achievement in Visual Effects, ...
    WEIGHTS = {u"award_category_name" : '2'}

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
    award_categories = models.ManyToManyField(Award_Category_Model)
    award_status = models.CharField(max_length = 31)
    imdb_id = models.CharField(max_length = 63)
    STATUSES = ["Won", "Nominated"]
    rank_value=0

    def __unicode__(self):
        return u'%s' % (self.award_name)

    #count ( sub , [ start , ] [ end ]) --> Int

    #Return the number of occurrences of substring sub in string s [ start : end ]. Optional                #arguments start and end are interpreted as in slice notation.

    #(rfind sub , [ start , ] [ end ]) --> int

    #Return the highest index in s where substring sub is found, such that sub is contained         #within s [ start : end ]. Optional arguments start and end are interpreted as in slice         #notation. Return -1 on failure.



    def basic_rank(self,search_word):
        '''
        This function perform a basic ranking based on a single word input

        INPUT :
                search_word
        OUTPUT :
                rank_value : the rank of the correspondent model according to the searched word
        '''

        
        WEIGHTS = {u"award_name" : 5}
        #u"award_categories" : 3,u"award_categories" : 2, u"awards_status" : 1
        tmp_rank=0

        #first I check if the search string is contained in the award_name
        if search_word in self.award_name.lower() :
            tmp_rank+=WEIGHTS["award_name"]*(float(len(search_word))/len(self.award_name)) #I multiply by a factor that takes into consideration the length of the search_word

        #Then I compute the number of occurences of search_string
        tmp_rank+=self.award_name.lower().count(search_word)

        #finally I check the position of the search string in the award_name
        index=self.award_name.lower().find(search_word)

        if index != -1 :
            tmp_rank+=((len(self.award_name) - index)/float(len(self.award_name)))*WEIGHTS["award_name"]
        # the float function inserted above is a trick to let python to consider the operands as float numbers rather than integers
        return tmp_rank


    def rank(self,search_string):
        '''
        This function perform a more complex ranking based on a string input by spliting the string into single words and combining the ranks computed for each word

        INPUT :
                search_string
        OUTPUT :
                rank_value : the rank of the correspondent model according to the searched string
        '''
        
		self.rank_value=0 #each time I have to rank an object I re-initialise its rank to 0
        tmp_rank=0
        search_string=search_string.lower()#I turn the string into lower case
        #I split the search_string into words
        words=search_string.split()
        #I transform words in a Set of unique words i.e ['the', 'man', 'gives', 'the', 'other', 'man', 'the', 'book'] becomes ['the','man','gives','other','book'] this is to avoid computing the basic_rank more than ones for the same word
        s=set(words)#this is a Set of unique words
        words=list(s) #I recover a list

        if len(words) > 1 :
            #If the string is composed of more than one word I first perform the rank considering the entire search_string
            tmp_rank+=self.basic_rank(search_string)

        #Now I compute seperate ranks
        for w in words:
            w_index=search_string.find(w) #it can't return -1 ^_^ so I can avoid the check
            tmp_rank+=self.basic_rank(w)*((len(search_string) - w_index)/float(len(search_string)))

            #the following computation has to be reviewed[could be optional because the scenario in which it really applies occurs seldom]
            occurs=search_string.count(w) #I compute the occurences of w in the search string,remember the case in which the user enters like search_string: 'Le fabuleux le ' we should take into account the fact that he entered twice the word 'le'
            tmp_rank+=float((occurs-1))/len(search_string) #I substract 1 so that in case the occurence is equal to 1 I don't increase the rank

        self.rank_value=tmp_rank
        return self.rank_value


class Actor_Model(models.Model):
    full_name = models.CharField(max_length = 255)
    nick_name = models.CharField(max_length = 127, null = True)
    birth_date = models.DateField(null = True)
    death_date = models.DateField(null = True)
    awards = [] # must be a list of Award_Model if any
    imdb_id = models.CharField(max_length = 63)
    mini_story = models.TextField(null = True)
    thumbnail_url = models.CharField(max_length = 255, null = True)
    place_of_birth = models.CharField(max_length = 127, null = True)
    place_of_death = models.CharField(max_length = 127, null = True)

    def __unicode__(self):
        return u'%s' %(self.full_name)

    def basic_rank(self,attribute_name,search_word):
        '''
        This function perform a basic ranking based on a single word input and works on string attributes of the model

        INPUT :
                search_word
        OUTPUT :
                rank_value : the rank of the correspondent model according to the searched word
        '''

        WEIGHTS = {u"full_name" : 5,u"nick_name":3}
        tmp_rank=0
        attribute_value=map(attrgetter(attribute_name),[self])[0] #gets the value of the attribute correspondent to attribute_name
        self.rank_value=0 #each time I have to rank an object I re-initialise its rank to 0


        #first I check if the search string is contained in the attribute_value
        if search_word in attribute_value.lower() :
            tmp_rank+=WEIGHTS[attribute_name]*(float(len(search_word))/len(attribute_value)) #I multiply by a factor that takes into consideration the length of the search_word

        #Then I compute the number of occurences of search_string
        tmp_rank+=attribute_value.lower().count(search_word)
        #the risk with this computation is that if the users enters "th" as search string it is likely that "th" occurs many times in a movie title,but this is not really a problem at the end

        #finally I check the position of the search string in the ref_attribute
        index=attribute_value.lower().find(search_word)

        if index != -1 :
            tmp_rank+=((len(attribute_value) - index)/float(len(attribute_value)))*WEIGHTS[attribute_name]
        # the float function inserted above is a trick to let python to consider the operands as float numbers rather than integers
        return tmp_rank


    def rank(self,search_string):
        '''
        This function perform a more complex ranking based on a string input by spliting the string into single words and combining the ranks computed for each word

        INPUT :
                search_string
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
            tmp_rank+=self.basic_rank("full_name",search_string)
            tmp_rank+=self.basic_rank("nick_name",search_string)

        #Now I compute seperate ranks
        for w in words:
            w_index=search_string.find(w) #it can't return -1 ^_^ so I can avoid the check
            tmp_rank+=self.basic_rank("full_name",w)*((len(search_string) - w_index)/float(len(search_string)))
            tmp_rank+=self.basic_rank("nick_name",w)*((len(search_string) - w_index)/float(len(search_string)))

            #the following computation has to be reviewed[could be optional because the scenario in which it really applies occurs seldom]
            occurs=search_string.count(w) #I compute the occurences of w in the search string,remember the case in which the user enters like search_string: 'Le fabuleux le ' we should take into account the fact that he entered twice the word 'le'
            tmp_rank+=float((occurs-1))/len(search_string) #I substract 1 so that in case the occurence is equal to 1 I don't increase the rank

        self.rank_value=tmp_rank
        return self.rank_value


class Writer_Model(models.Model):
    full_name = models.CharField(max_length = 255)
    nick_name = models.CharField(max_length = 127, null = True)
    birth_date = models.DateField(null = True)
    death_date = models.DateField(null = True)
    awards = [] # must be a list of Award_Model if any
    imdb_id = models.CharField(max_length = 63)
    mini_story = models.TextField(null = True)
    thumbnail_url = models.CharField(max_length = 255, null = True)
    place_of_birth = models.CharField(max_length = 127, null = True)
    place_of_death = models.CharField(max_length = 127, null = True)

    def __unicode__(self):
        return self.full_name
class Director_Model(models.Model):
    full_name = models.CharField(max_length = 255)
    nick_name = models.CharField(max_length = 127, null = True)
    birth_date = models.DateField(null = True)
    death_date = models.DateField(null = True)
    awards = [] # must be a list of Award_Model if any
    imdb_id = models.CharField(max_length = 63)
    mini_story = models.TextField(null = True)
    thumbnail_url = models.CharField(max_length = 255, null = True)
    place_of_birth = models.CharField(max_length = 127, null = True)
    place_of_death = models.CharField(max_length = 127, null = True)

    def __unicode__(self):
        return self.full_name

class Movie_Model(models.Model):
    original_title = models.CharField(max_length = 255)
    # the original title of the movie, in original country(ies)

    #original_countries = models.ManyToManyField(Country_Model)

    # the original movie country, from which it comes

    #awards = models.ManyToManyField(Award_Model, through = "Award_Matcher_Model")
    awards=[]
    # the awards of the movie (won or nominated, it has its importance)

    #actors = models.ManyToManyField(Actor_Model)
    actors=[]
    # actors of the movie
    #writers = models.ManyToManyField(Writer_Model)
    writers=[]
    # writers of the movie
    #directors = models.ManyToManyField(Director_Model)
    directors=[]
    # directors of the movie
    #genres = models.ManyToManyField(Genre_Model)
    genres=[]
    # action, thriller, love romance, ...
    runtime = models.CharField(max_length = 7, null = True)
    # time duration of the movie
    user_rating = models.CharField(max_length = 7, null = True)
    # user rating of the movie
    imdb_id = models.CharField(max_length = 63)
    # id of the movie on imdb - useful to decide whether a movie
    # is already or not in our database
    plot = models.TextField()
    # plot of the movie
    summary = models.TextField()
    # summary of the movie

    thumbnail_url = models.CharField(max_length = 255, null = True)
    # url of the thumbnail of the movie
    filename = models.CharField(max_length = 255)
    # name of movie on local disk
    extension = models.CharField(max_length = 31)
    # .avi, .mkv, .mpeg, ...
    path = models.CharField(max_length = 255)
    # path to movie on disk
    hash_code = models.CharField(max_length = 31)
    # hashcode of the movie
    movie_trailer_url = models.CharField(max_length = 255)
    # link to the trailer of the movie

    first_created = models.DateTimeField(auto_now = True)
    # datetime when movie was first created
    last_modified = models.DateTimeField(auto_now_add = True)
    # datetime when movie was last modified

    def __unicode__(self):
        return self.original_title
