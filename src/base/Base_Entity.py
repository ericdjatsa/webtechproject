'''
Created on 14 mars 2010

@author: Christophe
'''

class Base_Entity():
    """ Base structure for all data.entities
    """
    
    def __init__(self, model):
        """ @param Entity: model object
        """
        self.__model = model

    def update(self):
        self.__model.put()

    @classproperty
    def id():
        def fget(self): return str(self.__model.key())
        def fset(self, value): pass