""" Mum's Moovie Catalog
    Web Technologies, Spring Semester Project
    
    Developers :
        Christophe Duhamel
        Eric Djatsayo
        Qiang Meng
        ?
        
    Architecture Pattern : MVC (Model-View-Controller)
    
    Project Tree :
    
        Packages
            base
            core
            data
            view
                static
                templates
            
        - base :
            Regroup all classes that are expected to be used project-wide, and to be inherited, sort of "basket 
        of peer classes" that embody the "bases" of our project
        - core :
            In the MVC pattern, represent all layers between datas' ones and client side's request. The core is the pure
        logic mecanism of the app, completely decorrelated from any special type of data modeling or format of request.
        Contains of course all workflows, but also all material useful to process tasks that, by nature, "should not
        belong" to a single class or single workflow".
        - data :
            In the MVC pattern, represent all layers that touch the database and inject datas up to the logic core.
        This layer is model-dependent, and must work in a way that abstract this dependance to the core. To do so, and
        it is crucial, no raw models should never be injected to the core, only well formated data, encapsulated in standard
        format that we'll call entities, that are python objects carrying data in their attributes.
            - entities : transfert-long lifetime object, they intend to abstract the data model-dependent layer from
            the core.
            - repositories : interface between data and core layers, any call to datas from core or upper layers
            "should always go through and only through these particular classes". Consequently, all repository methods,
            who have a knowledge on the model-dependancy of the data layer, "shall never return models".
        - view :
            In the MVC pattern, correspond to the last layer between logic mecanism of the server and controller's
        input of the client (web user). Consequently, it is an interface between python "abstract" world of objects 
        and http "real" world of users. Then, data at this layer must change of carrier, so never a view method should
        render python objects.
        
        - static & templates : all static content interpreted or executed client-side.
    
    Extras :
        library : contains all frameworks needed (django, json ?).
        manage.py (or django-admin.py) : main file to pilot development with django (see infos on djangoproject.com).
        settings.py : main file to configure the features of the django project.
        
"""