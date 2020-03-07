#X = []
#Y = []
#
##insanely high data rates ($1000 or more per MB)
#omitted_countries = {'Yemen', 'Mauritania', 'Equatorial Guinea'}
#
#
##HDI regression with logarithmic shift
#for country in countryIncome:
#    if country in countryHDI and country in countryGDP and country in countriesMBps and country not in omitted_countries and country in countryRoads:
#        X.append([countryHDI[country], math.log(countryRoads[country])])
#
#for country in countriesMBps:
#    if country in countryHDI and country in countryGDP and country in countriesMBps and country not in omitted_countries and country in countryRoads:
#        Y.append(countriesMBps[country])
#
#
#X = np.array(X, dtype=float)
#Y = np.array(Y, dtype=float)
#Y = np.log(Y)
#
#
#HDIModel = sm.OLS(Y, X).fit()
#predictions = HDIModel.predict(X)
#print(HDIModel.summary())
#
#seabornInstance.distplot(Y, axlabel="$ Per MB/s", color="red")
#plt.show()
#
#test_space = np.linspace(0, 100)
#
#plt.plot(test_space, predictions)
#plt.scatter(test_space, Y, color="red")
#plt.show()



#
#test_space = np.linspace(-2, 10, 126)

# seabornInstance.distplot(Y, axlabel="$ Per MB/s", color="red")
# plt.show()

#
#plt.scatter(test_space, predictions)
#plt.scatter(test_space, Y, color="red")
#plt.show()

# plt.scatter(test_space, test_predictions)
# plt.show()


# create regression model
# compare with what we
# find data on wireless backhaul density
# avoid overfitting (by whatever method that andrew Ng taught us)

