'''
Created on 14 mars 2010

@author: Christophe
'''

from exceptions import NotImplementedError

class Individual_Model(WTP_Serializable_Model):
    """
    first_name : req
    last_name : req
    birth_date : req
    nick_name : if avail.
    death_date : if avail.
    """
    
    @classmethod
    def kind(cls):
        raise NotImplementedError
    
    def __init__(self, first_name, last_name, nick_name = None, birth_date, death_date = None):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        if nick_name is not None: self.nick_name = nick_name
        if death_date is not None: self.death_date = death_date