import sys
sys.path.insert(0, 'data')
from data import *
from toExcel import *


def countryMbps(countrySubCost, countryAvgSpeed):
    countriesMbps = {}
    for country in countrySubCost:
        if country in countryAvgSpeed:
            countriesMbps[country] = round(countrySubCost[country]/countryAvgSpeed[country], 2)
    return countriesMbps

def countryMktSize(countrySubCost, countrySubsCapita, countryRawPop):
    countriesMktSize = {}
    for country in countrySubCost:
        if country in countrySubsCapita and country in countryRawPop:
            countriesMktSize[country] = round(countrySubCost[country]*countrySubsCapita[country]*countryRawPop[country]/100, 2)
    return countriesMktSize

#income and population density data

def globalCountryMbps(countriesMbps):
    MbpsList = []
    for country in countriesMbps:
        MbpsList.append(countriesMbps[country])
    MbpsList.sort()
    print("Median Mbps = ${:,.2f}".format(round(MbpsList[len(MbpsList)//2], 2)))
    print("Average Mbps = ${:,.2f}".format(round(sum(MbpsList)/len(MbpsList), 2)))


def globalMrktSize(countriesMktSize):
    globalMrktSize = 0
    for country in countriesMktSize:
        globalMrktSize+=countriesMktSize[country]

    # take .019/.70 fraction of the market
#     (NSR Report on the fraction of satellite in backhaul)
    print("Wirless Global Market Size = ${:,.2f}".format(round(globalMrktSize, 2)))
    globalMrktSize*=(.019/.7)
    print("Satellite Global Market Size = ${:,.2f}".format(round(globalMrktSize, 2)))

    return globalMrktSize


subCost = costPerSub()
avgSpeed = speedPerCountry()
perCapSubs = subsPerCapita()
popSizes = rawPopPerCountry()
mbps = countryMbps(subCost, avgSpeed)
mktSizes = countryMktSize(subCost, perCapSubs, popSizes)

globalMrktSize(mktSizes)
globalCountryMbps(mbps)


def updateData():
    createWb("SatelliteInternetTAM")
    createSheet("SatelliteInternetTAM", "TAM Breakdown", 0)

    exportData = [["Country", "Average Subscription Cost", "Average Internet Speed", "Number of Subscribers"]]

    for country in popSizes:
        if country in subCost and country in avgSpeed and country in perCapSubs:
            exportData.append([country, round(subCost[country], 2), avgSpeed[country], perCapSubs[country]*popSizes[country]/100])

    addData("SatelliteInternetTAM", "TAM Breakdown", exportData)

updateData()
