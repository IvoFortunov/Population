import os
import requests
from Population import config
from .models import populationData


def getPopulationForCountry(code, year):
    #Get population for base year
    url = 'https://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?date={}&format=json'.format(code,year)
    print (url)
    r = requests.get(url)
    js =r.json()

    #if page==0 means no data
    if js[0].get('page')==0:
        return None

    list_data =js[1]

    countryCode = list_data[0].get('countryiso3code')
    countryName = list_data[0].get('country').get('value')
    pd = populationData(config.baseYear,countryCode,countryName)
    if list_data[0].get('indicator').get('id') == 'SP.POP.TOTL':
        #if value==None means no data
        val = list_data[0].get('value')
        if val==None:
            return None
        pd.population=int(val)
    
    #Get growths for several years back
    for y in range(config.baseYear-config.numYears+1, config.baseYear+1):
         url = 'https://api.worldbank.org/v2/country/{}/indicator/SP.POP.GROW?date={}&format=json'.format(code,y)
         print (url)
         r = requests.get(url)
         js =r.json()
         list_data =js[1]
         if list_data[0].get('indicator').get('id') == 'SP.POP.GROW':
            pd.growths.append(float(list_data[0].get('value')))
    return pd


def getPopulations(year):
    #Get population for base year
    url = 'https://api.worldbank.org/v2/country/ALL/indicator/SP.POP.TOTL;SP.POP.GROW?source=2&date={}&format=json&per_page=1000'.format(year)
    print (url)
    r = requests.get(url)
    js =r.json()
    
    #if page==0 means no data
    if js[0].get('page')==0:
        return None

    list_data =js[1]   

    pDatas={}
    for i in list_data:
       
        #Check for correct indicator
        if i.get('indicator').get('id') == 'SP.POP.TOTL':
            countryCode = i.get('countryiso3code') 
            countryName = i.get('country').get('value')
            if countryCode=='':
                continue
            if not countryCode in config.countryCodes:
                continue
            pd = populationData(config.baseYear,countryCode,countryName)
          
            #Add new data if not exist
            if not countryCode in pDatas:
                 pDatas[countryCode] = pd     
                 
            #Manage population indicator
            if i.get('indicator').get('id') == 'SP.POP.TOTL':
                try:
                    population=int(i.get('value'))
                except:
                    population=0
                pDatas[countryCode].population = population
            
    #Get growths for several years back
    for y in range(config.baseYear-config.numYears+1, config.baseYear+1):
        url = 'https://api.worldbank.org/v2/country/ALL/indicator/SP.POP.GROW?date={}&format=json&per_page=1000'.format(y)
        print (url)
        r = requests.get(url)
        js =r.json()
        list_data =js[1]

        for i in list_data:
            countryCode = i.get('countryiso3code') 
            if countryCode=='':
                    continue
            if not countryCode in config.countryCodes:
                    continue
            if i.get('indicator').get('id') == 'SP.POP.GROW':
                val = i.get('value')
                if not val == None:
                    pDatas[countryCode].growths.append(float(val))
             
     
    return pDatas

def getCountryList():
    
    return config.countryCodes
