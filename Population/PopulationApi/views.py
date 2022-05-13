from django.shortcuts import render
from django.http import JsonResponse
from Population import config
from .services import getPopulationForCountry, getPopulations, getCountryList
from .models import populationData
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['GET'])
def countryList(request):
    countries= getCountryList()
    [print(key,':',value) for key, value in countries.items()]
    return Response(countries, status.HTTP_200_OK)


@api_view(['GET'])
def getPopulationByCountry(request):
    try:
        code = request.GET['code']  
        year = int(request.GET['year'])
    except:
        return Response(status.HTTP_400_BAD_REQUEST)

    if year<config.baseYear:
        return Response("Year must be > {}!".format(config.baseYear) , status.HTTP_400_BAD_REQUEST)

    if not code in config.countryCodes:
        return Response("Bad country code", status.HTTP_400_BAD_REQUEST)



    pd = getPopulationForCountry(code,str(config.baseYear))

    if pd==None:
        return Response("No data!",status.HTTP_204_NO_CONTENT)
    
    pd.predict(year)
     
    res = pd.toDic()
    print(res)
    return Response(res,status.HTTP_200_OK)


@api_view(['GET'])
def getPopulationByYear(request):
    try:
        year = int(request.GET['year'])
    except:
        return Response('Invalid year!', status.HTTP_400_BAD_REQUEST)

    #check for paging
    try:
        page = int(request.GET['page'])
    except:
        page=1
    try:
        perpage = int(request.GET['perpage'])
    except:
        perpage=20

    if (year<config.baseYear):
        return Response("Year must be > {}!".format(config.baseYear) , status.HTTP_400_BAD_REQUEST)

    pDatas=getPopulations(str(config.baseYear))

    if pDatas==None:
        return Response("No data!",status.HTTP_204_NO_CONTENT)

    countries = []
    for pd in pDatas.values():
        pd.predict(year)
        countries.append(pd.toDic())
    countries.sort(key = lambda row: row['predictedPopultaion'],reverse=True)
    res = countries[(page-1)*perpage:page*perpage]
    print(*res, sep='\n')
    return Response(res,status.HTTP_200_OK)


def index(request):
    return render(request,'index.html')


