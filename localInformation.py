# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 13:26:20 2023

@author: HP
"""

import wolframalpha
app_id = 'T8R3RV-8P8A96E29H'


def localFinder(string, extrastring):

    client = wolframalpha.Client(app_id)

    res = client.query(string)

    res_lst=[]

    for pod in res.pods:
        for sub in pod.subpods:
            if(sub.plaintext!=None):
                res_lst.append(sub.plaintext)
    
    
    
    extrares = client.query(extrastring)
    extra_res_lst=[]
    for pod in extrares.pods:
        for sub in pod.subpods:
            if(sub.plaintext!=None):
                extra_res_lst.append(sub.plaintext)
                
    ansString = str(string) + '<br><br>'
    
    extraAnsString = str(extrastring) + '<br><br>'
    
    for i in range(len(res_lst)):
        ansString += str(res_lst[i])+'<br>'
        
    for i in range(len(extra_res_lst)):
        extraAnsString += str(extra_res_lst[i])+'<br>'
        
    return (ansString, extraAnsString)