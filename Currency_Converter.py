# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 15:55:03 2015

@author: APAX
"""

import urllib2
import json
import mysql.connector
import datetime

def UpdateTheDatabase(current_time, currency_from, currency_to, currency_input, Error):
    db = mysql.connector.connect(user='', password='',
                              host='',
                              database='')
    
    query="insert into Currency_Converter (Date_and_Time, Major_Currency, Minor_Currency, \
                                           Amount, Error) values (%s, %s, %s, %s, %s)"                                        
    data = (current_time, currency_from, currency_to, currency_input, Error)    
    cursor=db.cursor()
    cursor.execute(query, data)
    db.commit()
    

def CurrencyConverter(currency_from, currency_to, currency_input):
    yql_base_url = "https://query.yahooapis.com/v1/public/yql"
    yql_query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("'+currency_from+currency_to+'")'
    yql_query_url = yql_base_url + "?q=" + yql_query + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    current_time=datetime.datetime.now()
    try:
        yql_response = urllib2.urlopen(yql_query_url)
        try:
            yql_json = json.loads(yql_response.read())
            currency_output = currency_input * float(yql_json['query']['results']['rate']['Rate'])
            Error='NULL'            
            UpdateTheDatabase(current_time, currency_from, currency_to, currency_input, Error)            
            return currency_output
        except (ValueError, KeyError, TypeError):
            Error='JSON format error'            
            UpdateTheDatabase(current_time, currency_from, currency_to, currency_input, Error)              
            return "JSON format error"
    
    except IOError, e:
        if hasattr(e, 'code'):
            Error=e.code            
            UpdateTheDatabase(current_time, currency_from, currency_to, currency_input, Error)  
            return e.code
        elif hasattr(e, 'reason'):
            Error=e.reason
            UpdateTheDatabase(current_time, currency_from, currency_to, currency_input, Error)  
            return e.reason
 
#-----------------------------------

#things that needs to be done in future:
#Check OANDA and modify the script based on that
#Check the live figures against the results
#Check the currency codes, this script uses the one in Wikipedia
