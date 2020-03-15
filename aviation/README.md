# In-flight Wifi Market Size Calculation
## Pricing Strategies
Assuming that the price of an hourly connection scales relative to internet demand, two pricing strategies were implemented as estimates of the predicted revenue generated from each consumer. 
1. Per-capita income pricing: scales the cost of inflight internet relative to the per-capita income of the departure nation.
    American inflight wireless is about .013% of the nation’s per-capita income, which is hard-coded into the model. 
2. Adjusted data pricing scales the cost of inflight internet relative to the inflated price of ground-based internet. Average hourly data rate for inflight internet is about 37 times more expensive than ground-based internet -- this was hard-coded into the model. 

## TAM Calculation
The following methodology was undertaken: 
1. (Country’s Revenue Passenger Kilometers) X (Average Flight Cruising Speed) = National Flight Time (Hours)
2. (National Flight Time) X (Hourly Price Based on Pricing Strategy) = Country’s TAM ($)
3. Sum of all Country TAM = Global TAM ($) 


## Implications
Coupled with data on the profit margins for airplane companies, this estimates much revenue internet satellite operators can expect from in-flight internet contracts.
