'''
Created on 14 mars 2010

@author: Christophe
'''

from base.WTP_Exception import WTP_Exception

class Core_Layer_Exception(WTP_Exception):
    def __init__(self, message, innerException):
        WTP_Exception.__init__(self, message, innerException)