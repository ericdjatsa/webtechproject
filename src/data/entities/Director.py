'''
Created on 14 mars 2010

@author: Christophe
'''

from base.Base_Entity import Base_Entity

class Director(Base_Entity):
    
    def __init__(self, model):
        Base_Entity.__init__(self, model)