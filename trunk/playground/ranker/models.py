from django.db import models


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
	
	#Return the number of occurrences of substring sub in string s [ start : end ]. Optional 		#arguments start and end are interpreted as in slice notation.

	#(rfind sub , [ start , ] [ end ]) --> int

	#Return the highest index in s where substring sub is found, such that sub is contained 	#within s [ start : end ]. Optional arguments start and end are interpreted as in slice 	#notation. Return -1 on failure.

	
	
	def basic_rank(self,search_word):
		'''    
		This function perform a basic ranking based on a single word input
		   
		INPUT :
			search_word
		OUTPUT :
			rank_value : the rank of the correspondent model according to the searched word
		'''
		
		self.rank_value=0 #each time I have to rank an object I re-initialise its rank to 0
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
    
	@classmethod
	def kind(cls):
		return "Award_Model"
    
	@staticmethod
	def add_award_model(imdb_id, award_name, date_of_awarding, award_status):
		if award_status not in Award_Model.STATUSES: 
			award_status = None
			award_model = Award_Model(imdb_id = imdb_id, award_name = award_name,
				date_of_awarding = date_of_awarding, award_status = award_status)
			award_model.save()
		return award_model
    
	@staticmethod
	def get_award_model_by_id(award_id):
		try:
			award_model = Award_Model.objects.get(id = award_id)
		except Exception: return None
		return award_model
    
	@staticmethod
	def get_award_model_by_imdb_id(id):
		try:
			model = Award_Model.objects.get(imdb_id = id)
		except Exception: return None
		return model
    
	@staticmethod
	def delete_award_model(award_id):
		award_model = Award_Model.get_country_model_by_id(award_id)
		if award_model is None: return False
		else:
			award_model.delete()
			return True
