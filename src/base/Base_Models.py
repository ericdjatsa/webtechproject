'''
Created on 14 mars 2010

@author: Christophe
'''

class Individual_Model(WTP_Serializable_Model):
    """
    first_name : req
    last_name : req
    nick_name : if avail.
    birth_date
    death_date : if avail.
    crawled_date
    """
    
    @classmethod
    def kind(cls):
        raise NotImplementedError
    
    def __init__(self, first_name, last_name, nick_name = None, birth_date, death_date = None, crawled_date):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.crawled_date = crawled_date
        if nick_name is not None: self.nick_name = nick_name
        if death_date is not None: self.death_date = death_date
        self.is_data_fresh = True
        

class WTP_Serializable_Model(db):
    """
        Base class for all the models that need to take advantage of 
        serialization
        Serialized representation of a model must be stored in dataXml attribute
        
        Each data update invalidates xmlDataValid attribute (False) indicating that
        reserialization is required
        
        !! xmlDataValid attribute MUST be manipulated through the calls to setXmlDataValid 
           and not directly
           
        !! children of this class cannot be updated via db.put()
           THEY MUST ALWAYS CALL THEIR NATIVE put() method instead
    """
    xmlDataValid = db.BooleanProperty(default=False)
    dataXml = db.TextProperty() 
     
    def put(self):
        """
            each put invalidates xmlDataValidAttribute
        """
        self.xmlDataValid = False
        return db.Model.put(self)
    
    def delete(self):
        """
            deletion is accompanied by invalidating parent's xml markup
        """
        theParent = self.parent() 
        if theParent is not None: 
            @transaction
            def trnsct():
                theParent.xmlDataValid = False
                theParent.put()
                return db.Model.delete(self)
            return trnsct()
        else:
            return db.Model.delete(self)
    
    def setXmlDataValid(self, value):
        """
            method used to manipulate the xmlDataValid attribute
            !! MUST NOT MANIPULATE xmlDataValid attribute directly
        """
        self.xmlDataValid = value
        db.Model.put(self)

    def serializeModel(self, xmlData = None):
        """
            if overloaded by children must be done the following way
            
            def serializeModel(self):
                xml = blah blah 
                return WTP_Serializable_Model.serializeModel(self,xml)
        """
        if xmlData is None:
            self.dataXml = self.to_xml()
        else: self.dataXml = xmlData
        
        self.setXmlDataValid(True)
        
        return self.dataXml
