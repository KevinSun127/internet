import pandas as pd
import numpy as np
import warnings
import re
import math
import matplotlib.pyplot as plt
import seaborn as seabornInstance
import statsmodels.api as sm
import itertools

def speedPerCountry():
    countryAvgSpeed = {}
    speedPerCountry = open('data/speed_per_country.txt').read()
    speedPerCountry = re.findall(r'([A-Z][A-Za-z\s]+)\s(\d+.[0-9]{2})', speedPerCountry, re.MULTILINE)
    for countryPair in speedPerCountry:
        countryAvgSpeed[countryPair[0]]= float(countryPair[1])
    return countryAvgSpeed


def subsPerCapita():
    countrySubsCapita = {}
    subsPerCountry = open('data/subs_per_country.txt').read()
    subsPerCountry = re.findall(r'([A-Z][A-Za-z\s]+)\s(\d+.\d+)', subsPerCountry, re.MULTILINE)
    for countryPair in subsPerCountry:
        countrySubsCapita[countryPair[0]] = float(countryPair[1])
    return countrySubsCapita


def rawPopPerCountry():
    data3 = pd.read_excel('data/countryRawPop.xlsx')
    countries3 = data3['Country']
    population = data3['Population']
    countryRawPop = {}
    for i in range(len(countries3)):
        countryRawPop[countries3[i]] = float(population[i])
    return countryRawPop


def countryToRegion():
    dataCosts = pd.read_excel('data/pricePerGB.xlsx')
    countryNames = dataCosts['Name']
    regionNames = dataCosts['Region']
    countryRegion = {}
    for (country, region) in zip(countryNames, regionNames):
        countryRegion[country] = region
    return countryRegion


def dataPerSubPerRegion():
    popPerCountry = rawPopPerCountry()
    countrySubsCapita = subsPerCapita()
    regions = countryToRegion()

    #take the number of people/100
    #multply by the number of broaband contract per 100
    #total number of regional contracts
    regionSubs = {"ASIA PACIFIC": 0, "MIDDLE EAST AND AFRICA": 0, "CENTRAL AND EASTERN EUROPE": 0,  "NORTH AMERICA": 0, "WESTERN EUROPE": 0, "LATIN AMERICA": 0}
    for country in countrySubsCapita:
        if country in popPerCountry and country in regions:
            regionSubs[regions[country]]+=(popPerCountry[country]/100*countrySubsCapita[country])

    regionDataUsage = {}
    data = pd.read_excel('data/dataTraffic.xlsx')
    regionNames = data['Region']
    dataTraffic = data['Monthly Data Traffic (GB)']
    for (traffic, region) in zip(dataTraffic, regionNames):
        regionDataUsage[region] = float(traffic)
    
    
    dataPerSub = {}
    for region in regionDataUsage:
        dataPerSub[region] = regionDataUsage[region]/regionSubs[region]
    
    return dataPerSub


def costPerSub():
    dataPerSub = dataPerSubPerRegion()
    countrySubCost = {}
    dataCosts = pd.read_excel('data/pricePerGB.xlsx')
    countryNames = dataCosts['Name']
    regionNames = dataCosts['Region']
    avgPrice = dataCosts['Average price of 1GB (USD)']
    for (price, region, country) in zip(avgPrice, regionNames, countryNames):
        # price per GB * total GB used per contract in that region
        if region in dataPerSub:
            countrySubCost[country] = float(price[1:])*dataPerSub[region]

    return countrySubCost


def HDIPerCountry():
    countryHDI = {}
    hdiPerCountry = open('data/hdi_data.txt').read()
    hdiPerCountry = re.findall(r'([A-Z][A-Za-z\s]+)\s(\d+.[0-9]{2})', hdiPerCountry, re.MULTILINE)
    for countryPair in hdiPerCountry:
        countryHDI[countryPair[0]]= float(countryPair[1])
    return countryHDI


def roadsPerCountry():
    countryRoads = {}
    roadsPerCountry = open('data/countryPavedRoads.txt').read()
    roadsPerCountry = re.findall(r'([A-Z][A-Za-z ]+)\t\ntotal:\s(\d+,\d+)', roadsPerCountry, re.MULTILINE)
    for countryPair in roadsPerCountry:
        countryRoads[countryPair[0]]=float(countryPair[1].replace(',', ''))
    return countryRoads


def incomePerCountry():
    data1 = pd.read_excel('data/countryIncomePop.xlsx')
    countries = data1['Country']
    incomes = data1['Median Income (USD)']
    countryIncome = {}
    for (country, income) in zip(countries, incomes):
        countryIncome[country] = float(income)
    return countryIncome


def popDensityPerCountry():
    data1 = pd.read_excel('data/countryIncomePop.xlsx')
    countries = data1['Country']
    popDensities = data1['Pop Density Per Km']
    countryPopDensity = {}
    for (country, popDensity) in zip(countries, popDensities):
        countryPopDensity[country] = float(popDensity)
    return countryPopDensity


def gdpPerCountry():
    data2 = pd.read_excel('data/countryGDP.xlsx')
    countries2 = data2['Country']
    gdp = data2['GDP Per Capita']
    countryGDP = {}
    for i in range(len(countries2)):
        countryGDP[countries2[i]] = float(gdp[i])
    return countryGDP
