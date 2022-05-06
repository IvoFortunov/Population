from django.db import models

# Create your models here.


class populationData(object):

    def __init__(self, baseYear, countryCode, countryName):
        self.countryCode = countryCode
        self.countryName = countryName
        self.population=0
        self.growths=[]
        self.growth=0.0
        self.predictedPopulation=0
        self.targetYear = 0
        self.baseYear = baseYear

    def predict(self,year):
        years = year - self.baseYear

        if len(self.growths)>0:
            self.growth = sum(self.growths)/len(self.growths)
        else:
            self.growth=0
        percentGrowth = (1+self.growth/100.0)**years
        self.predictedPopulation =int(self.population*percentGrowth)
        self.targetYear = year
        return self.predictedPopulation

   

    def toDic(self):
        dic = {
                "countryCode" : self.countryCode,
                "countryName" : self.countryName,
                "targetYear" : self.targetYear,
                "predictedPopultaion" : self.predictedPopulation,
                "population" : self.population,
                "growth" : self.growth
                 #"growths" : self.growths
            }
        return dic

