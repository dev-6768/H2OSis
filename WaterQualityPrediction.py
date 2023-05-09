# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:34:50 2023

@author: HP
"""

import pandas as pd
#from sklearn.ensemble import AdaBoostRegressor
import pickle

dataset = pd.read_csv('water_potability.csv')
#print(dataset.head())

# m1 = AdaBoostRegressor()

model = pickle.load(open("./model.pkl", 'rb'))

def Predictor(a1,a2,a3,a4,a5,a6,a7,a8, a9):
    countPotable=0
    countNotPotable=0
    
    #dataset1 = dataset.drop(['Potability'], axis=1)
    #target = dataset['Potability']
    
    
    #m1.fit(dataset1, target)
    
    # AdaBoostRegressor(base_estimator=None, learning_rate=1.0, loss='linear',
    #                   n_estimators=50, random_state=None)
    
    #m1.score(dataset1, target) * 100
    
    # for i in range(500):
    #     predictValue = model.predict([[a1,a2,a3,a4,a5,a6,a7,a8,a9]])[0]
    #     if(predictValue<=0.7):
    #         countNotPotable+=1
        
    #     else:
    #         countPotable+=1
    pred = model.predict([[a1,a2,a3,a4,a5,a6,a7,a8,a9]])[0]

    if pred > 0.7:
        return "The water will be consumable after basic filtration."
    else:
        return "The water needs extensive treatment to be consumable"
        
    # return (countPotable, countNotPotable)

def Accurator(pair):
    if(pair[0]>pair[1]):
        return 'The water is safe for consumption.'
    
    elif(pair[0]<=pair[1]):
        return 'The water is not safe for consumption'


#print(Predictor(8.31676588421467, 214.373394085622, 22018.4174407752, 8.05933237743854, 356.886135643056, 363.266516164243, 18.4365244954933, 100.34167436508, 4.62877053683708))