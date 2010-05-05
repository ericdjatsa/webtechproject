'''
Created on 14 mars 2010

@author: Christophe
'''

from exceptions import Exception


class WTP_Exception(Exception):
    """
        base exception class
    """
    def __init__(self, message, innerException = None):
        Exception.__init__(self)
        self.message = message
        self.innerException = innerException
    
    def __str__(self):
        res = self.message
        if self.innerException is not None:
            res = res + (" inner exception: %s" % self.innerException)
        return res