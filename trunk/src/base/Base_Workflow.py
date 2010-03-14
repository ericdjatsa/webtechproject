'''
Created on 14 mars 2010

@author: Christophe
'''

from core.Core_Layer_Exception import Core_Layer_Exception
from core.tools.routines import isValidInt
from core.tools.routines import isValidDate

from data.repositories import *

class Base_Workflow():

    """
        All the derived workflows are used in the same manner (god bless polymorphism)

        1. creation
                myWorkflow = MyWorkflow(request-params, pipes)
        2. make it work
                myWorkflow.work()
        3. catch invalid input exception
                WorkflowInputNotValidException
           inspect myWorkflow.response()["invalid_fields"] or myWorkflow.getInvalidFields()
           these methods return a dictionary with field_name => comment for all the fields that are invalid
        4. inspect myWorkflow.response() to get all the related data to build the response page
           each workflow can alternatively provide shortcuts to access both request/response data

           e.g. myWorkflow.userId gives myWorkflow.request()["user-id"]
    """

    def __init__(self, requestParameters, authorizationPipe, loggingPipe = None, data_pipe = Repository(),
                 taskManager = TaskManager()):
        """
            initialize workflow : provide request parameters, authorization pipe (based on interface)
        """
        self.__data_pipe = data_pipe
        self.__request = request_parameters
        self.__response = {}
        self.__response["invalid_fields"] = {}
        self.isInputValid = True

    def request(self):
        return self.__request

    def isInRequest(self, fieldName):
        return self.__request.has_key(fieldName)

    def fieldIsNotEmpty(self, fieldName):
        if self.isInRequest(fieldName):
            if self.request()[fieldName] != "" and self.request()[fieldName]:
                return True
            else: return False
        else: return False

    def dataPipe(self):
        return self.__dataPipe

    def response(self):
        return self.__response

    def add2Response(self, key, value):
        self.__response[key] = value

    def registerInvalidField(self, fieldName, comments):
        self.__response["invalid_fields"][fieldName] = comments
        self.isInputValid = False

    def getInvalidFields(self):
        return self.__response["invalid_fields"]

    def validateFieldNotNull(self, fieldName):
        if self.request().has_key(fieldName):
            if self.request()[fieldName] is not None: return True
        
        self.registerInvalidField(fieldName, "field value is empty")
        return None

    def validateStringFieldNotEmpty(self, fieldName):

        if not self.request().has_key(fieldName): value = None
        else: value = self.request()[fieldName]

        if value is None or value == "" :
            self.registerInvalidField(fieldName, "string value is empty")
            return False
        else: return True

    def validateIntField(self, fieldName):

        if not self.request().has_key(fieldName) : value = None
        else: value = self.request()[fieldName]

        if not isValidInt(value):
            self.registerInvalidField(fieldName, "invalid number")
            return False
        else: return True

    def validateDateField(self, fieldName):

        if not self.request().has_key(fieldName): value = None
        else : value = self.request()[fieldName]

        if not isValidDate(value):
            self.registerInvalidField(fieldName, "invalid date")
            return False
        else: return True

    def validateFieldValueInRange(self, fieldName, range):

        if not self.request().has_key(fieldName): value = None
        else : value = self.request()[fieldName]

        if value in range : return True
        else :
            self.registerInvalidField(fieldName, "value is not supported")
            return False

    def validateInput(self):
        """
            perform input validation, requestParameters are validated (+ permissions based on the authorization)

            all the invalid fields names must be put to response["invalid_fields"] via registerInvalidField

        """
        raise NotImplementedError

    def process(self):
        """
            perform the core workflow task based on the input provided via request parameters and based on the
            authorization permissions and status

            returned is a dictionary of parameters that will be used to render the resulting page
            the workflow can also terminate by throwing an exception
        """
        raise NotImplementedError

    def work(self):
        """
           is called by a view directly

           @raise WorkflowInputNotValidException: workflow input is invalid
                                                  the list of invalid fields with additional comments can be obtained from response["invalid_fields"] (dictionary)
        """

        self.validateInput()
        if not self.isInputValid : raise WorkflowInputNotValidException()

        self.process()

        return self.__response

class WorkflowInputNotValidException(Exception):
    def __init__(self):
        pass