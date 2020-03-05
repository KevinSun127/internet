import pandas as pd
import numpy as np
import warnings
import re
import math
import matplotlib.pyplot as plt
import seaborn as seabornInstance
import statsmodels.api as sm

costPerSub = open('cost_per_sub.txt').read()
speedPerCountry = open('speed_per_country.txt').read()
subsPerCountry = open('subs_per_country.txt').read()
hdiPerCountry = open('hdi_data.txt').read()

countrySubCost = {}
countryAvgSpeed = {}
countrySubsCapita = {}
countryHDI = {}

costPerSub = re.findall(r'([A-Z][A-Za-z\s]+)\s(\d+.[0-9]{2})', costPerSub, re.MULTILINE)
for countryPair in costPerSub:
    countrySubCost[countryPair[0]] = float(countryPair[1])


subsPerCountry = re.findall(r'([A-Z][A-Za-z\s]+)\s(\d+)', subsPerCountry, re.MULTILINE)
for countryPair in subsPerCountry:
    countrySubsCapita[countryPair[0]] = float(countryPair[1])


speedPerCountry = re.findall(r'([A-Z][A-Za-z\s]+)\s(\d+.[0-9]{2})', speedPerCountry, re.MULTILINE)
for countryPair in speedPerCountry:
    countryAvgSpeed[countryPair[0]]= float(countryPair[1])

hdiPerCountry = re.findall(r'([A-Z][A-Za-z\s]+)\s(\d+.[0-9]{2})', hdiPerCountry, re.MULTILINE)
for countryPair in hdiPerCountry:
    countryHDI[countryPair[0]]= float(countryPair[1])

countriesMBps = {}

for country in countrySubCost:
    if country in countryAvgSpeed:
        countriesMBps[country] = round(countrySubCost[country]/countryAvgSpeed[country], 2)

countriesMktSize = {}

for country in countrySubCost:
    if country in countrySubsCapita:
        countriesMktSize[country] = round(countrySubCost[country]*countrySubsCapita[country], 2)


#try to create a regression with population density, etc.
#
# pricing per country
print(countriesMBps)

#market sizes per 100 inhabitants
print(countriesMktSize)

data1 = pd.read_excel('countryIncomePop.xlsx')
countries = data1['Country']
income = data1['Median Income (USD)']
population = data1['Pop Density Per Km']

countryIncome = {}
countryPop = {}

for i in range(len(countries)):
    countryIncome[countries[i]] = income[i]
    countryPop[countries[i]] = population[i]


data2 = pd.read_excel('countryGDP.xlsx')
countries2 = data2['Country']
gdp = data2['GDP Per Capita']


countryGDP = {}
for i in range(len(countries2)):
    countryGDP[countries2[i]] = gdp[i]

X = []
Y = []

#insanely high data rates ($1000 or more per MB)
omitted_countries = {'Yemen', 'Mauritania', 'Equatorial Guinea'}


#HDI regression with logarithmic shift
for country in countryIncome:
    if country in countryHDI and country in countryGDP and country in countriesMBps and country not in omitted_countries:
        X.append([countryHDI[country]])

for country in countriesMBps:
    if country in countryHDI and country in countryGDP and country in countriesMBps and country not in omitted_countries:
        Y.append(math.log(countriesMBps[country]))


X = np.array(X, dtype=float)
X = np.log(X)
Y = np.array(Y, dtype=float)

HDIModel = sm.OLS(Y, X).fit()
predictions = HDIModel.predict(X)
print(HDIModel.summary())


test_space = np.linspace(-2, 10, 126)

# seabornInstance.distplot(Y, axlabel="$ Per MB/s", color="red")
# plt.show()


plt.scatter(test_space, predictions)
plt.scatter(test_space, Y, color="red")
plt.show()


for country in countryIncome:
    if country in countryHDI and country in countryGDP and country in countriesMBps and country not in omitted_countries:
        X.append([countryHDI[country]])

for country in countriesMBps:
    if country in countryHDI and country in countryGDP and country in countriesMBps and country not in omitted_countries:
        Y.append(math.log(countriesMBps[country]))


X = np.array(X, dtype=float)
X = np.log(X)
Y = np.array(Y, dtype=float)


test_space = np.linspace(-2, 10, 126)

# seabornInstance.distplot(Y, axlabel="$ Per MB/s", color="red")
# plt.show()


plt.scatter(test_space, predictions)
plt.scatter(test_space, Y, color="red")
plt.show()

# plt.scatter(test_space, test_predictions)
# plt.show()


# create regression model
# compare with what we
# find data on wireless backhaul density
# avoid overfitting (by whatever method that andrew Ng taught us)
