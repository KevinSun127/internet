# Wirless Broadband Market Size Calculation
## Methodology
Used the following datasets:<br />
1. Mobile broadband subscriptions per 100 people by country
2. Total population by country
3. Mobile data traffic in GB by region (Asia Pacific, Middle East and Africa, Central and Eastern Europe, North America, Western Europe, Latin America)
4. Price per GB by country
5. Average speed of internet by country

To calculate the total number of subscribers in a country, multiplied each country's the number of broadband subscriptions per 100 people by the total population divided by 100. <br />

To calculate the data usage per subscription, divided the total mobile data traffic in a region by the total number of subscribers in a region. <br />

To calculate the price per contract, multiplied the data usage per subscription by the price per GB for each country. <br />

Regional TAM was estimated by multiplying the value of each contract with the number of total contracts in each region. Global TAM was a sum of the regional TAM estimates. <br />

Price per Mbps for each country was estimated by dividing each country's price per contract by their average speed of internet. The median price per Mbps was taken as a rough estimate of a global pricing strategy, since the data was heavily left skewed. 


