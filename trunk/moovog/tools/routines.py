'''
Created on 19 avr. 2010

@author: Christophe
'''

from tools.dateutil.parser import parse

def isValidDate(dateString):
    """
        checks if provided date string contains a valid date
    """
    if dateString is None or dateString == "" : return False
    try:
        d = parse(dateString)
        return True
    except Exception, x: return False
    
def isValidInt(intString):
    """
        returns True if the intString is a valid string representation of an integer
    """
    try:
        i = int(intString)
        return i is not None
    except Exception, x : return False
    
def isValidTime(timeString):
    """ 
        returns True if the timeString contains a valid time
    """
    pass