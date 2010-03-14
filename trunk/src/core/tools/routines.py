'''
Created on 14 mars 2010

@author: Christophe
'''

from core.Core_Layer_Exception import Core_Layer_Exception

def isValidDate(dateString):
    """ Checks if provided date string contains a valid date
    """
    
    if dateString is None or dateString == "" : return False
    
    try:
        d = parse(dateString)
        return True
    except Core_Layer_Exception, x: return False

def isValidInt(intString):
    """ Returns True if the intString is a valid string representation of an integer
    """
    
    try:
        i = int(intString)
        return i is not None
    except Core_Layer_Exception, x : return False