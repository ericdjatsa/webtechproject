# -*- coding: utf-8 -*-

def parse_countries(string,table):
    country = ''
    j=0
    if (len(table) == 0):
        while (string[j]!='-'):
            j+=1        
    else:
        while (string[j]!=','):
            j+=1
            if (j==len(string)):
                return table
  
    j+=2
    
    while (string[j]!=',' and string[j]!=':' and string[j]!='('):
        country = country+string[j]
        j+=1
        if (j==len(string)):
            table.append(country)
            return table
  
    if (string[j]=='('):
        country = country[:len(country)-1]
    table.append(country)
    parse_countries(string[j:],table)

def parse_aka(string):

    #returned dic
    returned = {}
    
    #list of countries
    countries = []
    returned['countries'] = countries

    aka = ''
    j = 1
    while (string[j] != '"'):
        aka = aka + string[j]
        j=j+1
    
    returned['aka']=aka

    parse_countries(string[j:],countries)
    
    returned['countries'] = countries
    return returned

def another_aka_parser(aka_list):
    result = {}
    country = []
    for aka_string in aka_list:
        aka_fragments = aka_string.rpartition("-")
        country_string = aka_fragments[2].lstrip()
        country_string = aka_fragments[2].rstrip()
        country.append(country_string)
        
        aka_string_fragment = aka_fragments[0]
        # go ahead an build a clean function
    return result