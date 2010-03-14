'''
Created on 14 mars 2010

@author: Christophe
'''

from core.Core_Layer_Exception import Core_Layer_Exception

class Workflow_Layer_Exception(Core_Layer_Exception):
    def __init__(self, message, innerException):
        Core_Layer_Exception.__init__(self, message, innerException)