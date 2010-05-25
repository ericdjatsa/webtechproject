# -*- coding: utf-8 -*-
#Ranking methods,to embed into seeker.repository(at the end of the class Repository for example
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
            #WEIGHTS = {u"original_title" : 5,u"akas":3} #I would love to do this but akas is not a field in Movie it is
            #inside a dictionnary
            WEIGHTS = {u"original_title" : 5}
        elif models_type=='Award_Model' :
            WEIGHTS = {u"award_name" : 5}

        
        attributes=list(WEIGHTS)
        
        mods={} #dictionnary key=models_str_representation value=models rank_value
        sorted_models=[]
        
        for mod in models_list :
            
            rnk=Repository.compute_rank(mod,attributes,search_string,WEIGHTS) #this is the first computation of the rank
            
            if models_type=='Movie_Model' :
                
                #create fictitious akas attributes like : akas_International,akas_UK,etc...
                #or after the attrgetter in basic_rank add : if attribute_name.startswith('akas') then search in the akas dictionary
                attributes.extend(["akas_International", "akas_France"])
                WEIGHTS["akas_International"]=3
                WEIGHTS["akas_France"]=3
                
                #Now computations based on akas,user_rating,awards etc...
                #update rnk
               
                akas_dict={}
                akas_dict=mod.infos["akas"]
                
                #for (k,v) in akas_dict.iteritems() :
                    #print 'i ',i
                    #print '(k,v)','(',k,':',v,')'
                    
                rnk+=Repository.compute_rank(mod,attributes[1:],search_string,WEIGHTS) #I skip the first attribute which is original_title because I've already computed the rank based on it above
                
                #Taking into account the user rating could provide a wrong ranking to the models because a movie can we very well rated by the users but be irelevant for the search_string
                #To solve this issue,I assign to the movie's original_title attribute a very high weight with respect to the user rating weight
                WEIGHTS["user_rating"]=1
                rnk+=float(mod.user_rating)*WEIGHTS["user_rating"]
                  
            elif models_type=='Award_Model' :
                print ''        
                #based on number of connections to the award
                #update rnk
                WEIGHTS["award_categories"]=0.5
                rnk+=len(mod.award_categories)*WEIGHTS["award_categories"]
                
                
            mods[str(mod)]=rnk
        
        #print '\n\nmods dictionnary',mods
        
        sorted_models=sorted(models_list,key=lambda mod:mods.get(str(mod)),reverse=True)
        return sorted_models #returns a list of sorted models according to decreasing rank 
