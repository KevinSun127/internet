import sys
sys.path.insert(0, 'data')

from data import np, math, pd, sm, plt, HDIPerCountry, costPerSub, speedPerCountry
from pricing import byCountryMbps

#Road regression with logarithmic shift

countryHDI = HDIPerCountry()
countriesMbps = byCountryMbps(costPerSub(), speedPerCountry())

omitted_countries = {'Yemen', 'Mauritania', 'Equatorial Guinea'}

X = []
Y = []

for country in countryHDI:
    if country in countriesMbps and country not in omitted_countries:
        X.append([math.log(countryHDI[country])])

for country in countriesMbps:
    if country in countryHDI and country not in omitted_countries:
        Y.append(math.log(countriesMbps[country]))

X = np.array(X, dtype=float)
Y = np.array(Y, dtype=float)
HDIModel = sm.OLS(Y, X).fit()
predictions = HDIModel.predict(X)


plt.plot(X, predictions)
plt.scatter(X, Y, color="red")


print(HDIModel.summary())
plt.show()

