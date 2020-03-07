import sys
sys.path.insert(0, 'data')
from data import *
from toExcel import *


def byCountryMbps(countrySubCost, countryAvgSpeed):
    countriesMbps = {}
    for country in countrySubCost:
        if country in countryAvgSpeed:
            countriesMbps[country] = round(countrySubCost[country]/countryAvgSpeed[country], 2)
    return countriesMbps

def byCountryMktSize(countrySubCost, countrySubsCapita):
    countriesMktSize = {}
    for country in countrySubCost:
        if country in countrySubsCapita:
            countriesMktSize[country] = round(countrySubCost[country]*countrySubsCapita[country], 2)
    return countriesMktSize

#income and population density data

def globalCountryMBps(countriesMBps):
    MbpsList = []
    for country in countriesMBps:
        MbpsList.append(countriesMBps[country])
    MbpsList.sort()
    print("Median MBps = ${:,.2f}".format(round(MbpsList[len(MbpsList)//2], 2)))
    print("Average MBps = ${:,.2f}".format(round(sum(MbpsList)/len(MbpsList), 2)))


def globalMrktSize(countriesMktSize, countryRawPop):
    globalMrktSize = 0
    for country in countriesMktSize:
        if country in countryRawPop:
            countriesMktSize[country]*=countryRawPop[country]/100
            globalMrktSize+=countriesMktSize[country]
                
    # take .019/.70 fraction of the market
    # (NSR Report on the fraction of satellite in backhaul)
    globalMrktSize*=(.019/.7)
    print("Satellite Global Market Size = ${:,.2f}".format(round(globalMrktSize, 2)))

    return globalMrktSize


def aggData(countrySubCost, countrySubsCapita, countryAvgSpeed):
    MBps = byCountryMBps(countrySubCost, countryAvgSpeed)
    MktSize = byCountryMktSize(countrySubCost, countrySubsCapita)

    MBpsList = []
    MBpsList.append(["Mobile Broadband Subscription Monthly Plan Price Per Country ($)",
                   "Average Internet Speed (MB/s)",
                   "Price Per MB/s"])

    MrktSizeList = []
    MrktSizeList.append("Mobile Broadband Subscription Costs Per Country ($)")


mbps = byCountryMbps(costPerSub(), speedPerCountry())
globalCountryMBps(a)
globalMrktSize(byCountryMktSize(costPerSub(), subsPerCapita()), rawPopPerCountry())

