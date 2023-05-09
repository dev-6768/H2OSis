# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:05:16 2023

@author: HP
"""

# import wolframalpha
# app_id = 'T8R3RV-8P8A96E29H'

# def localFinder(string):
#     client = wolframalpha.Client(app_id)
#     res = client.query(string)
#     res_lst=[]
#     for pod in res.pods:
#         for sub in pod.subpods:
#             if(sub.plaintext!=None):
#                 res_lst.append(sub.plaintext)
                
#     ansString = ''
    
#     for i in range(len(res_lst)):
#         ansString += str(res_lst[i])+"\n"
        
#     return ansString

# print(localFinder(""))

def cityData(locationCity):
    if(locationCity in ["Ranchi", "Mumbai", "Delhi", "Chennai", "Kolkata"]):
        return 1
    else:
        return 0
    


indexedDict={
    "Ranchi":[0,1,2,3,4,5,6,7,8,9,10,11,12],
    "Mumbai":[21,22,23,24,25,26,27,44,45],
    "Delhi":[13,14,15,16,17,18,19,20,42,43],
    "Chennai":[28,29,30,31,32,33,34,48,49],
    "Kolkata":[35,36,37,38,39,40,41,46,47]   
}

import pandas as pd
df = pd.read_csv("LocationWaterStations.csv")

dataList=[]
dataLatitude=[]
dataLongitude=[]
dataName = []

def searcher(locationCity):
    indexedList = indexedDict[locationCity]
    for i in indexedList:
        dataLatitude.append(df['Lat'][i])
        dataLongitude.append(df['Lon'][i])
        dataName.append(df['Name'][i])
    
    dataList.append(dataLatitude)
    dataList.append(dataLongitude)
    dataList.append(dataName)
    
    return dataList

def utilityListFunction(listObject):
    ans = "<p>To know more information about routes to nearest water startions, starting from the nearest : <br>"
    for i in listObject:
        ans += '<a href="' + i + '">Click here</a><br>'
    
    ans += '</p>'
    return ans
