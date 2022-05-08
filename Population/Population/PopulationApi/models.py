from django.db import models
from Population import config

# Create your models here.


class populationData(object):

    def __init__(self, baseYear, countryCode, countryName):
        self.countryCode = countryCode
        self.countryName = countryName
        self.population=0
        self.growths=[]
        self.growth=0.0
        self.predictedPopulation=0
        self.predictedPopulation2=0
        self.targetYear = 0
        self.baseYear = baseYear

    def predict(self,year):
        years = year - self.baseYear

        if len(self.growths)>0:
            self.growth = sum(self.growths)/len(self.growths)            
        else:
            self.growth=0
           
        #Calculate population according to compound intrerest or exponentiam model
        if config.useCompoundInterest:    
            percentGrowth = (1+self.growth/100.0)**years
            self.predictedPopulation =int(self.population*percentGrowth)
        else:
            percentGrowth = config.num_e**(years*self.growth/100)
            self.predictedPopulation =int(self.population*percentGrowth)

        self.targetYear = year
        return self.predictedPopulation

   
   
        
    def toDic(self):
        dic = {
                "countryCode" : self.countryCode,
                "countryName" : self.countryName,
                "startPopulation" : self.population,
                "targetYear" : self.targetYear,
                "growth" : self.growth,
                "predictedPopultaion" : self.predictedPopulation
                
                 #"growths" : self.growths
            }
        return dic

