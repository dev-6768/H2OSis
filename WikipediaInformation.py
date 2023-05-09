# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 21:41:52 2023

@author: HP
"""

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import geocoder
import geopy
from googlesearch import search

def wikipediaInfo(locationCity, locationCountry):
    
    nominatim = Nominatim()
    areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
    
    nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
    
    getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
    
    
    overpass = Overpass()
    query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
    result = overpass.query(query)
    
    firstElement = result.elements()[0]
    
    sdf = firstElement.geometry()['coordinates'][0]
    
    pair = (str(sdf[0][0]), str(sdf[0][1]))
    
    first = str(pair[1])
    second = str(pair[0])
    
    locationObject = geopy.geocoders.Nominatim(user_agent="GetLoc")
    locationCurr = locationObject.reverse(first + ", " + second)
    
    addressString = locationCurr.raw['display_name']
    resultList= []
    
    for searchvariable in search(addressString, tld="com", num=10, stop=10, pause=2):
        # resultList += '<a href=' + '"' + searchvariable + '"' + '>' + searchvariable + '</a>' + '<br>'
        resultList.append(searchvariable)
        
    return resultList

#print(wikipediaInfo('Sydney', 'Australia'))