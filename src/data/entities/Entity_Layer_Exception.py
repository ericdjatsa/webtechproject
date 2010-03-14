'''
Created on 14 mars 2010

@author: Christophe
'''

from data.Data_Layer_Exception import Data_Layer_Exception

class Entity_Layer_Exception(Data_Layer_Exception):
    def __init__(self, message, innerException):
        Data_Layer_Exception.__init__(self, message, innerException)