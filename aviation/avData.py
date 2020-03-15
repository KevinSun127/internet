import pandas as pd
import re
import math
import itertools
import sys
sys.path.insert(0, 'data')
from toExcel import *

# take all countries's median income

def perCapitaIncomePerCountry():
    data1 = pd.read_excel('data/countryIncomePop.xlsx')
    countries = data1['Country']
    incomes = data1['Median Income (USD)']
    countryIncome = {}
    for (country, income) in zip(countries, incomes):
        countryIncome[country] = float(income)
    return countryIncome


# map those countries into regions

def countryToRegion():
    dataCosts = pd.read_excel('data/pricePerGB.xlsx')
    countryNames = dataCosts['Name']
    regionNames = dataCosts['Region']
    countryRegion = {}
    for (country, region) in zip(countryNames, regionNames):
        countryRegion[country] = region
    return countryRegion


#take all countries raw population

def rawPopPerCountry():
    data3 = pd.read_excel('data/countryRawPop.xlsx')
    countries3 = data3['Country']
    population = data3['Population']
    countryRawPop = {}
    for i in range(len(countries3)):
        countryRawPop[countries3[i]] = float(population[i])
    return countryRawPop


#take the average income across the region

def avgIncomePerRegion(countryCapita, countryPop, regions):
    regionIncomes = {"ASIA PACIFIC": [0, 0], "MIDDLE EAST AND AFRICA": [0, 0], "CENTRAL AND EASTERN EUROPE": [0, 0],  "NORTH AMERICA": [0, 0], "WESTERN EUROPE": [0, 0], "LATIN AMERICA": [0, 0]}
    for country in countryCapita:
        if country in regions and country in countryPop:
            regionIncomes[regions[country]][0]+=countryCapita[country]*countryPop[country]
            regionIncomes[regions[country]][1]+=countryPop[country]

    for region in regionIncomes:
        regionIncomes[region] = regionIncomes[region][0]/regionIncomes[region][1]

    return regionIncomes


# number of passengers per country

def passengersPerCountry():
    data = pd.read_excel('data/flightTraffic.xlsx')
    countryNames = data['Name']
    passengerCounts = data['Passengers']
    countryPassengers= {}
    for (country, passengerCount)  in zip(countryNames, passengerCounts):
        countryPassengers[country] = passengerCount
    return countryPassengers


# passengers per region

def passengersPerRegion():
    countryPassengers = passengersPerCountry()
    regions = countryToRegion()
    regionPassengers = {"ASIA PACIFIC": 0, "MIDDLE EAST AND AFRICA": 0, "CENTRAL AND EASTERN EUROPE": 0,  "NORTH AMERICA": 0, "WESTERN EUROPE": 0, "LATIN AMERICA": 0}
    for country in countryPassengers:
        if country in regions:
            regionPassengers[regions[country]]+=countryPassengers[country]
    return regionPassengers



# 1. take total online internet hours in each region
# 2. divide that by the total number of passengers
# 3. price it accordingly
#       a. .00013 of the country's per capita income per hour
#       b.  average data usage per hour * price of data in that country
# 4. multiply by the total population in each region



# from excel:
def usagePerPassenger():
    regionInternetHours = {"ASIA PACIFIC": 0.195851163*1000000000, "MIDDLE EAST AND AFRICA": 0.063595349*1000000000, "CENTRAL AND EASTERN EUROPE": 0.148013953*1000000000,  "NORTH AMERICA": 0.126065116*1000000000, "WESTERN EUROPE": 0.148013953*1000000000, "LATIN AMERICA": 0.028702326*1000000000}
    totalPassengers = passengersPerRegion()
    perPassengerHour = {}
    for region in regionInternetHours:
        if region in totalPassengers:
            perPassengerHour[region] = regionInternetHours[region]/totalPassengers[region]
    return perPassengerHour


#progressive pricing based on .013% of the country's per capita income per hour
def progressivePricing(regionIncome):
    regionInternetHours = {"ASIA PACIFIC": 0.195851163*1000000000, "MIDDLE EAST AND AFRICA": 0.063595349*1000000000, "CENTRAL AND EASTERN EUROPE": 0.148013953*1000000000,  "NORTH AMERICA": 0.126065116*1000000000, "WESTERN EUROPE": 0.148013953*1000000000, "LATIN AMERICA": 0.028702326*1000000000}
    perCapitaTAM = {}
    globalTAM = 0
    for region in regionIncome:
        perCapitaTAM[region] = regionInternetHours[region]*0.00013*regionIncome[region]
        globalTAM+=regionInternetHours[region]*0.00013*regionIncome[region]
    print("In-flight Aviation Global TAM [Progressive Pricing] = ${:,.2f}".format(round(globalTAM, 2)))
    return perCapitaTAM


# helper function to determine how much data is used in a region
def subsPerCapita():
    countrySubsCapita = {}
    subsPerCountry = open('data/subs_per_country.txt').read()
    subsPerCountry = re.findall(r'([A-Z][A-Za-z\s]+)\s(\d+.\d+)', subsPerCountry, re.MULTILINE)
    for countryPair in subsPerCountry:
        countrySubsCapita[countryPair[0]] = float(countryPair[1])
    return countrySubsCapita


# average rate of data usage per month per region
def avgDataPerRegion():
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


def perPassengerHourlyData(timePerPassenger, dataPerMonthPerPerson):
    regionPassDataUse = {}
    for region in timePerPassenger:
        regionPassDataUse[region] = timePerPassenger[region]*dataPerMonthPerPerson[region]/(30*24)
    return regionPassDataUse


# data price per month is 37 times more expensive than average broadband
#   explain that
def inflatedDataBasedPricing():
    regionPassDataUse = perPassengerHourlyData(usagePerPassenger(), avgDataPerRegion())
    countryWifiCost = {}
    countryPass = passengersPerCountry()
    
    dataCosts = pd.read_excel('data/pricePerGB.xlsx')
    countryNames = dataCosts['Name']
    regionNames = dataCosts['Region']
    avgPrice = dataCosts['Average price of 1GB (USD)']
    
    globalTAM = 0
    for (price, region, country) in zip(avgPrice, regionNames, countryNames):
        # price per GB * total GB used per contract in that region
        if region in regionPassDataUse and country in countryPass:
            countryWifiCost[country] = float(price[1:])*regionPassDataUse[region]*countryPass[country]*.77*37
            globalTAM+=float(price[1:])*regionPassDataUse[region]*countryPass[country]*.77*37
    print("In-flight Aviation Global TAM [Data-Usage Pricing] = ${:,.2f}".format(round(globalTAM, 2)))
    return countryWifiCost


def pricePerGB():
    GBPrice = {}
    dataCosts = pd.read_excel('data/pricePerGB.xlsx')
    countryNames = dataCosts['Name']
    regionNames = dataCosts['Region']
    avgPrice = dataCosts['Average price of 1GB (USD)']
    for (price, country) in zip(avgPrice, countryNames):
        GBPrice[country] = float(price[1:])
    return GBPrice


progressivePricing(avgIncomePerRegion(perCapitaIncomePerCountry(), rawPopPerCountry(), countryToRegion()))


inflatedDataBasedPricing()


def updateData():
    regions = countryToRegion()
    avgRegDataPerMonth = avgDataPerRegion()
    passDataUsage = perPassengerHourlyData(usagePerPassenger(), avgDataPerRegion())
    passCount = passengersPerCountry()
    passTime = usagePerPassenger()
    dataPrice = pricePerGB()
    perCapIncome = perCapitaIncomePerCountry()
    createWb("AviationTAM")
    createSheet("AviationTAM", "TAM Breakdown", 0)
    
    exportData = [["Country", "National Inflight Data Usage (GB)",
                   "National Passenger Flight Time (Hours)", "Average Per GB Internet Cost (USD)", "Per Capita Income Pricing (USD)" ]]

    for country in regions:
        if country in passCount and country in dataPrice and country in perCapIncome:
            exportData.append([country, passDataUsage[regions[country]]*passCount[country]*.77, passTime[regions[country]]*passCount[country], dataPrice[country], perCapIncome[country]*0.00013])
                  
    addData("AviationTAM", "TAM Breakdown", exportData)


updateData()

#"Total Inflight Wifi Revenue (USD)", "Total Data Usage", "$ Per Mbps"
