import yfinance as yf
import numpy as np
import random as random
import matplotlib.pyplot as plt
from scipy.stats._continuous_distns import norm
"""
    Yfinance allows us to pull historical stock data
    numpy will help with calculting changes in stock price
"""
    
ticker = yf.Ticker('SPY')
    
#we will generate 10 years of SPY data
start_date = '2012-05-04'
end_date = '2022-05-04'
historical_data = ticker.history(start=start_date, end=end_date)
print(historical_data.head())
    
historical_data = historical_data[['Close']]
print(historical_data)

historical_data['Close'].plot(title='SPY Stock Price', ylabel='Closing Price [$]', figsize=[10,6])
plt.grid()

#create lists to hold Days, Price, and %change
days = [i for i in range(1, len(historical_data['Close'])+1)]
orig_price = historical_data['Close'].tolist()
change = historical_data['Close'].pct_change().tolist()[1:]

#derive the mean and std deviation of the percenter change day to day
mean = np.mean(change)
std = np.std(change)
print('\nMean percent change: ' +str(round(mean*100,2))+'%') 
print('Standard Deviation ofpercent change: ' +str(round(std*100,2))+'%')


#Then Choose an aribitrary number of monte carlo sims to run (higher the better)
#additionally choose the number of days to simulate, I chose 252 as it is the number of trading days in a year
sims = 200
simDays = 1*252

#Create the figure to plot the simulations
fig = plt.figure(figsize=[10,6])
plt.plot(days, orig_price)
plt.title("Monte Carlo Stock Prices [" +str(sims)+"simulations]")
plt.xlabel("Trading Days After" +start_date)
plt.ylabel("Closing Price [$]")
plt.xlim([200, len(days)+simDays])
plt.grid()

#create lists to hold the end date closing prices from each sim and the number of sims with a higher closing price

ending_closings=[]
ending_above_close = []

#run the number of simulations desired
for i in range(sims):
    numDays = [days[-1]]
    closingPrice = [historical_data.iloc[-1,0]]
    
    #predict the number of days for this simulation
    for j in range(simDays):
        numDays.append(numDays[-1]+1)
        r = random.random()
        percchange = norm.ppf(r, loc=mean, scale=std)
        closingPrice.append(closingPrice[-1]*(1+percchange))
    
    if closingPrice[-1]>orig_price[-1]:
        ending_above_close.append(1)
    else:
        ending_above_close.append(0)
    ending_closings.append(closingPrice[-1])
    plt.plot(numDays, closingPrice)
    
avgClosePrice = sum(ending_closings)/sims
avgPercentChange = (avgClosePrice-orig_price[-1])/orig_price[-1]

probOfIncrease = sum(ending_above_close)/sims

print('\n Predicted closing price after '+ str(sims)+ ' simulation: $'+str(round(avgClosePrice, 2)))
print('Predicted percenter increase after 1 year: ' +str(round(avgPercentChange, 2)))
print('Probability of stock price increasing after 1 year: ' + str(round(probOfIncrease, 2))+'%')

plt.show
