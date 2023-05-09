# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:13:25 2023

@author: HP
"""

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import geopy
import geocoder
import folium
import csvFileTester
import pandas as pd
import time
import routingLocation
import haversineDistanceCalculator

def finder(locationCity, locationCountry):

    # if(locationCity=="" or locationCountry==""):
        
    #     geocoderObject = geocoder.ip('me')
    #     first = str(geocoderObject.latlng[0])
    #     second = str(geocoderObject.latlng[1])
        
    #     locationObject = geopy.geocoders.Nominatim(user_agent="GetLoc")
    #     locationCurr = locationObject.reverse(first + ", " + second)
    #     locationCity = locationCurr.raw['address']['city']
    #     locationCountry = locationCurr.raw['address']['country']
        
    nominatim = Nominatim()
    areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
    
    nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
    
    getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
    
    
    overpass = Overpass()
    query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
    result = overpass.query(query)
    
    
    resTempStorage = result.elements()
    
    if(resTempStorage != []):
        firstElement = result.elements()[0]
        sdf = firstElement.geometry()['coordinates'][0] 
    #print(firstElement.geometry()['coordinates'][0])
    
    else:
        sdf = [[]]
    
    if(sdf[0]!=[]):
        
        dct = {}
        device = list(range(101, 101+len(sdf)))
        dct['GPSLat']=[]
        dct['GPSLng']=[]
        dct['device']=[]
        
        i=0
        for data in sdf:
            dct['device'].append(device[i])
            dct['GPSLat'].append(data[0])
            dct['GPSLng'].append(data[1])
            i+=1    
                    
        lati = getLoc.latitude
        longi = getLoc.longitude
        
        mapObj = folium.Map(location = [lati, longi], zoom_start = 12)
        
        
        for i in range(len(dct['device'])):
            latitude = float(dct['GPSLat'][i])
            longitude = float(dct['GPSLng'][i])
            folium.CircleMarker(location = [longitude, latitude], 
                                radius = 5, popup = "Water Body No. "+str(i+1)).add_to(mapObj)
        
        mapObj.save('templates/mapData.html')
        
    else:
        lati = getLoc.latitude
        longi = getLoc.longitude
        
        mapObj = folium.Map(location = [lati, longi], zoom_start=12)
        
        mapObj.save("templates/mapData.html")

    
def waterStation(locationCity, locationCountry):
    if(csvFileTester.cityData(locationCity)):
            
        dataArray = csvFileTester.searcher(locationCity)
        dctCoordinates={"lat":dataArray[0], "lon":dataArray[1], "name":dataArray[2]}
        #dctNameCoordinates = {"lat":dataArray[0], "lon":dataArray[1]}
        
        sizeColor = len(dataArray[0])
        
        dctCoordinates['device'] = [101]*sizeColor
        
        nominatim = Nominatim()
        areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
        
        nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
        
        getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
        
        lati = getLoc.latitude
        longi = getLoc.longitude
        
        mapObj = folium.Map(location = [lati, longi], zoom_start = 12)
        
        distanceVariableDct = {}
        distanceVariableLst = []
        
        coordinateURLList=[]
        for i in range(len(dctCoordinates['device'])):
            
            longitude = float(dctCoordinates['lon'][i])
            latitude = float(dctCoordinates['lat'][i])
            
            urlGenerator = routingLocation.coordinateRouteFunction((lati, longi), (latitude, longitude))
            
            sourceDistance = haversineDistanceCalculator.haversine(longi, lati, longitude, latitude)#routingLocation.nearestDistanceFinder((lati, longi), (latitude, longitude))
            
            if((sourceDistance not in distanceVariableDct)):
                distanceVariableDct[sourceDistance] = [urlGenerator]
                
            else:
                distanceVariableDct[sourceDistance].append(urlGenerator)
            
            folium.CircleMarker(location = [latitude, longitude], 
                                radius = 5, popup = "Water Station : " + dctCoordinates['name'][i]).add_to(mapObj)
            
        for x in distanceVariableDct:
            distanceVariableLst.append(x)
        
        distanceVariableLst.sort()
        
        for x in distanceVariableLst:
            for y in distanceVariableDct[x]:
                coordinateURLList.append(y)
        
        mapObj.save('templates/waterStations.html')
        
        return coordinateURLList
        
    else:
        nominatim = Nominatim()
        areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
        
        nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
        
        getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
        
        lati = getLoc.latitude
        longi = getLoc.longitude
        
        mapObj = folium.Map(location = [lati, longi], zoom_start = 12)
        
        mapObj.save('templates/waterStations.html')
        
        
        
    
def drinkingWaterFinder(locationCity, locationCountry):
    nominatim = Nominatim()
    areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
    
    nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
    
    getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
    
    
    overpass = Overpass()
    query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector='"man_made"="wastewater_plant"', includeGeometry=True)
    result = overpass.query(query)
    
    resTempStorage = result.elements()
    
    if(resTempStorage != []):
        firstElement = result.elements()[0]
        sdf = firstElement.geometry()['coordinates'][0] 
    #print(firstElement.geometry()['coordinates'][0])
    
    else:
        sdf = [[]]
    
    if(sdf[0]!=[]):
    
        dct = {}
        device = list(range(101, 101+len(sdf)))
        dct['GPSLat']=[]
        dct['GPSLng']=[]
        dct['device']=[]
        
        i=0
        for data in sdf:
            dct['device'].append(device[i])
            dct['GPSLat'].append(data[0])
            dct['GPSLng'].append(data[1])
            i+=1    
                    
        lati = getLoc.latitude
        longi = getLoc.longitude
        
        mapObj = folium.Map(location = [lati, longi],
        								zoom_start = 12)
        
        
        for i in range(len(dct['device'])):
            latitude = float(dct['GPSLat'][i])
            longitude = float(dct['GPSLng'][i])
            folium.CircleMarker(location = [longitude, latitude], 
                                radius = 5, popup = "Wastewater treatment plant "+str(i+1)).add_to(mapObj)
        
        mapObj.save('templates/drinkingWaterFinder.html')
        
    else:
        lati = getLoc.latitude
        longi = getLoc.longitude
        mapObj = folium.Map(location = [lati,longi], zoom_start=12)
        mapObj.save("templates/drinkingWaterFinder.html")
    
    
def waterTapFinder(locationCity, locationCountry):
    nominatim = Nominatim()
    areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
    
    nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
    
    getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
    
    
    overpass = Overpass()
    query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector='"man_made"="water_tap"', includeGeometry=True)
    result = overpass.query(query)
    
    resTempStorage = result.elements()
    
    if(resTempStorage != []):
        firstElement = result.elements()[0]
        sdf = firstElement.geometry()['coordinates'][0] 
    #print(firstElement.geometry()['coordinates'][0])
    
    else:
        sdf = [[]]
    
    if(sdf[0]!=[]):
    
        dct = {}
        device = list(range(101, 101+len(sdf)))
        dct['GPSLat']=[]
        dct['GPSLng']=[]
        dct['device']=[]
        
        i=0
        for data in sdf:
            dct['device'].append(device[i])
            dct['GPSLat'].append(data[0])
            dct['GPSLng'].append(data[1])
            i+=1    
                    
        lati = getLoc.latitude
        longi = getLoc.longitude
        
        mapObj = folium.Map(location = [lati, longi],
        								zoom_start = 12)
        
        
        for i in range(len(dct['device'])):
            latitude = float(dct['GPSLat'][i])
            longitude = float(dct['GPSLng'][i])
            folium.CircleMarker(location = [longitude, latitude], 
                                radius = 5, popup = "Drinking Water Station No. "+str(i+1)).add_to(mapObj)
        
        mapObj.save('templates/waterTapFinder.html')
        
    else:
        lati = getLoc.latitude
        longi = getLoc.longitude
        mapObj = folium.Map(location = [lati,longi], zoom_start=12)
        mapObj.save("templates/waterTapFinder.html")

def anyGeneralWaterBodyFinder(locationCity, locationCountry, selectorArgument, popupArgument, fileSaveName):
    nominatim = Nominatim()
    areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
    
    nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
    
    getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
    
    overpass = Overpass()
    
    try:
        query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector=selectorArgument[0], includeGeometry=True)
        result = overpass.query(query)
        
        queryRiver = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector=selectorArgument[1], includeGeometry=True)
        riverResult = overpass.query(queryRiver)
        
        time.sleep(1)
        
        
        queryWasteWater = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector=selectorArgument[2], includeGeometry=True)
        wasteWaterResult = overpass.query(queryWasteWater)
        
        queryLake = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector=selectorArgument[3], includeGeometry=True)
        lakeResult = overpass.query(queryLake)
        
        
        resTempStorage = result.elements()
        riverResTempStorage = riverResult.elements()
        wasteWaterResultTempStorage = wasteWaterResult.elements()
        lakeResultTempStorage = lakeResult.elements()
        
        if(resTempStorage != []):
            firstElement = result.elements()[0]
            sdf = firstElement.geometry()['coordinates'][0] 
            varsdf = sdf[0][::-1]
            
        else:
            sdf=[[]]
            varsdf = 0
            
        if(riverResTempStorage != []):
            firstRiverElement = riverResTempStorage[0]
            sdf2 = firstRiverElement.geometry()['coordinates'][0] 
            varsdf2 = sdf2[0][::-1]
            
        else:
            sdf2=[[]]
            varsdf2 = 0
            
        if(wasteWaterResultTempStorage != []):
            firstWasteWaterElement = wasteWaterResultTempStorage[0]
            sdf3 = firstWasteWaterElement.geometry()['coordinates'][0]
            varsdf3 = sdf3[0][::-1]
            
        else:
            sdf3=[[]]
            varsdf3 = 0
            
            
        if(lakeResultTempStorage != []):
            firstLakeElement = lakeResultTempStorage[0]
            sdf4 = firstLakeElement.geometry()['coordinates'][0]
            varsdf4 = sdf4[0][::-1]
            
        #print(firstElement.geometry()['coordinates'][0])
        
        else:
            sdf4 = [[]]
            varsdf4 = 0
            
        for x in sdf2:
            sdf.append(x)
            
        for x in sdf3:
            sdf.append(x)
            
        for x in sdf4:
            sdf.append(x)
            
        #print(sdf)
        
        if(sdf[0]!=[]):
        
            dct = {}
            device = list(range(101, 101+len(sdf)))
            dct['GPSLat']=[]
            dct['GPSLng']=[]
            dct['device']=[]
            
            i=0
            for data in sdf:
                if(data!=[]):
                    dct['device'].append(device[i])
                    dct['GPSLat'].append(data[0])
                    dct['GPSLng'].append(data[1])
                    i+=1    
                        
            lati = getLoc.latitude
            longi = getLoc.longitude
            
            mapObj = folium.Map(location = [lati, longi],
            								zoom_start = 12)
            
            print(dct)
            for i in range(len(dct['device'])):
                latitude = float(dct['GPSLat'][i])
                longitude = float(dct['GPSLng'][i])
                folium.CircleMarker(location = [longitude, latitude], 
                                    radius = 5, popup = popupArgument+str(i+1)).add_to(mapObj)
            
            mapObj.save(fileSaveName)
            
            outputLst = []
            
            if(varsdf!=0):
                outputLst.append(varsdf)
            
            if(varsdf2!=0):
                outputLst.append(varsdf2)
                
            if(varsdf3!=0):
                outputLst.append(varsdf3)
                
            if(varsdf4!=0):
                outputLst.append(varsdf4)
            
            return outputLst
            
        else:
            lati = getLoc.latitude
            longi = getLoc.longitude
            mapObj = folium.Map(location = [lati,longi], zoom_start=12)
            mapObj.save(fileSaveName)
            return []
    
    except:
        return "Request Failed !"
        

def generalBodyFinder(locationCity, locationCountry):
    selectorArgument = ['"water"="river"', '"water"="lake"', '"natural"="water"', '"water"="pond"']
    popupArgument = "Water Body No. "
    fileSaveName = "templates/generalWaterBodyFile.html"
    locationTuple = anyGeneralWaterBodyFinder(locationCity, locationCountry, selectorArgument, popupArgument, fileSaveName)
    
    if(locationTuple!=[] and locationTuple!="Request Failed !"):
    
        centralLocation = routingLocation.locationRouteFinder(locationCity, locationCountry)
        
        urlString1 = routingLocation.coordinateRouteFunction(centralLocation, locationTuple[0])
        urlString2 = routingLocation.coordinateRouteFunction(centralLocation, locationTuple[1])
        urlString3 = routingLocation.coordinateRouteFunction(centralLocation, locationTuple[2])
        urlString4 = routingLocation.coordinateRouteFunction(centralLocation, locationTuple[3])
        
        return [urlString1, urlString2, urlString3, urlString4]
    
    else:
        return [0,0,0,0]
    
    
    
    
    
    
    
    