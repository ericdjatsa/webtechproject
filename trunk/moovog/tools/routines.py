'''
Created on 19 avr. 2010

@author: Christophe
'''

from tools.dateutil.parser import parse
import datetime

#def isValidDate(dateString):
#    """
#        checks if provided date string contains a valid date
#    """
#    if dateString is None or dateString == "" : return False
#    try:
#        d = parse(dateString)
#        return True
#    except Exception, x: return False

def isValidDate(date):
    reference = datetime.date.today()
    return date.__class__ in reference.__class__.mro()
    
def isValidInt(intString):
    """
        returns True if the intString is a valid string representation of an integer
    """
    try:
        i = int(intString)
        return i is not None
    except Exception, x : return False
    
def isValidFloat(floatString):
    """
        returns True if the floatString
    """
    try:
        f = float(floatString)
        return f is not None
    except Exception, x: return False
    
def isValidTime(timeString):
    """ 
        returns True if the timeString contains a valid time
    """
    reference = datetime.time(hour=1)
    return timeString.__class__ in reference.__class__.mro()

def areListEqual(list1, list2):
    """
        returns True if the lists are equal (same length, same values)
    """
    a = []
    if len(list1) == len(list2):
        list1.sort()
        list2.sort()
        for i in range(0, len(list1)):
            if list1[i] != list2[i]:
                return False
        return True
    else:
        return False
    
def special_dictionary_merger(dict_a, dict_b):
    """
        merges 2 dictionaries, this function is symmetric
    """
    for k in dict_a.keys():
        if dict_b.has_key(k):
            try:
                # simple tests to know if dict_a[k] and dict_b[k] are lists
                dict_a[k].reverse()
                dict_b[k].reverse()
                for thing in dict_a[k]:
                    if thing not in dict_b[k]:
                        dict_b[k].append(thing)
            except Exception: continue
        else: dict_b[k] = dict_a[k]
    return dict_b