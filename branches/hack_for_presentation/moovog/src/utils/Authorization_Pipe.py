'''
Created on 6 mai 2010

@author: Christophe
'''

class Authorization_Pipe:
    
    def __init__(self, user):
        self.__user = user
        
    def _user(self):
        return self.__user
    
    def get_user_id(self):
        return self._user().id