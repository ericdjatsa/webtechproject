'''
Created on 14 mars 2010

@author: Christophe
'''

from tools.routines import *
from src.utils.Authorization_Pipe import Authorization_Pipe
from src.utils.clean_name import cleanName

from src.seeker.repository import Repository

class Base_Workflow():

    """
        All the derived workflows are used in the same manner (god bless polymorphism)

        1. creation
                myWorkflow = MyWorkflow(request-params, authorizationPipe)
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

    def __init__(self, input, authorization_pipe, data_pipe = Repository()):
        """
            initialize workflow : provide request parameters, authorization pipe (based on interface)
        """
        self.__request = input
        self.__response = {}
        self.__response["invalid_fields"] = {}
        self.is_input_valid = True
        self.__repository = data_pipe
        self.__authorization_pipe = authorization_pipe

    def request(self):
        return self.__request

    def is_in_request(self, fieldName):
        return self.__request.has_key(fieldName)

    def field_is_not_empty(self, fieldName):
        if self.isInRequest(fieldName):
            if self.request()[fieldName] != "" and self.request()[fieldName]:
                return True
            else: return False
        else: return False
        
    def repository(self):
        return self.__repository

    def response(self):
        return self.__response
    
    def authorization(self):
        return self.__authorization_pipe

    def add_to_response(self, key, value):
        self.response()[key] = value

    def register_invalid_field(self, fieldName, comments):
        self.response()["invalid_fields"][fieldName] = comments
        self.is_input_valid = False

    def get_invalid_fields(self):
        return self.__response["invalid_fields"]
    
    def string_cleaner(self, fieldName):
        return cleanName(fieldName)

    def validate_field_not_null(self, fieldName):
        if self.request().has_key(fieldName):
            if self.request()[fieldName] is not None: return True
        
        self.register_invalid_field(fieldName, "field value is empty")
        return None
    
    def validate_list_field_not_empty(self, fieldName):
        if not self.request().has_key(fieldName): value = None
        else: value = self.request()[fieldName]

        if value is None or value == []:
            self.register_invalid_field(fieldName, "list value is empty")
            return False
        else: return True 

    def validate_string_field_not_empty(self, fieldName):
        if not self.request().has_key(fieldName): value = None
        else: value = self.request()[fieldName]

        if value is None or value == "":
            self.register_invalid_field(fieldName, "string value is empty")
            return False
        else: return True

    def validate_int_field(self, fieldName):
        if not self.request().has_key(fieldName) : value = None
        else: value = self.request()[fieldName]

        if not isValidInt(value):
            self.register_invalid_field(fieldName, "invalid number")
            return False
        else: return True
        
    def validate_float_field(self, fieldName):
        if isValidFloat(self.request()[fieldName]):
            return True
        else:
            self.register_invalid_field(fieldName, "invalid float")
            return False
        
    def validate_time_field(self, fieldName):
        if isValidTime(self.request()[fieldName]):
            return True
        else:
            self.register_invalid_field(fieldName, "invalid time")
            return False

    def validate_date_field(self, fieldName):
        if not self.request().has_key(fieldName): value = None
        else : value = self.request()[fieldName]

        if not isValidDate(value):
            self.register_invalid_field(fieldName, "invalid date")
            return False
        else: return True

    def validate_field_value_in_range(self, fieldName, range):
        if not self.request().has_key(fieldName): value = None
        else : value = self.request()[fieldName]

        if value in range : return True
        else :
            self.register_invalid_field(fieldName, "value is not supported")
            return False

    def validate_input(self):
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
        self.validate_input()
        if not self.is_input_valid : raise WorkflowInputNotValidException()
        self.process()
        return self.response()

class WorkflowInputNotValidException(Exception):
    def __init__(self):
        pass