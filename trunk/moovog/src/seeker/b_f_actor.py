'''
Created on 29 avr. 2010

@author: Christophe
'''

import httplib
import json
import datetime

def hit_the_server(server, url, port, method='POST'):
    httpServ = httplib.HTTPConnection(server, port)
    httpServ.connect()
    httpServ.request(method, url)
    response = httpServ.getresponse()
    
    if response.status == httplib.OK:
        to_response = response.read()
        httpServ.close()
        return to_response
    else:
        print response.status
        httpServ.close()
        print "something's wrong with the http response"

#actor_attributes = {}
#actor_attributes["first-name"] = "john"
#actor_attributes["last-name"] = "doe"
#actor_attributes["birth-date"] = str(datetime.date.today())
#response = hit_the_server("localhost", "/seeker/__fake-actor/", 8000, json.JsonWriter().write(actor_attributes))
response = hit_the_server("localhost", "/seeker/__fake-actor/", 8000)
print response