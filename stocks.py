from numpy import std
from math import sqrt
from pandas import read_csv


#Load the CSV using pandas
def loadCSV(csvPath):
    return(read_csv(csvPath))
 
#Return the Anual return rates
def avgAnnual(myCSV):
    first = myCSV['Adj Close'][len(myCSV['Date'])-1]
    last = myCSV['Adj Close'][0]
    return ((last/first)-1)
 
#Get a list of the Daily return rates
def getDailyRets(myCSV):
    dailyRets = []
    for i in range (0, len(myCSV)-1):
        dailyRets.append(myCSV['Adj Close'][i]/myCSV['Adj Close'][i+1] - 1)
    return (dailyRets)
 
#Return the average Daily return rate
def avgDaily(myCSV):
    return (sum(getDailyRets(myCSV))/len(myCSV))
 
#Get the standart deviation of the average daily rates
def dailyRetsStdev(myCSV):
    return std(getDailyRets(myCSV))
 
#Get the Sharpe Ratio
def sharpeRatio(myCSV):
    return (sqrt(len(myCSV))*avgDaily(myCSV)/dailyRetsStdev(myCSV))
 
#Return Anual return rates, Average Daily Return Rate, St Dev and Sharpe Ratio
def stockStats(myCSV, stock_code):
    csv_file = myCSV
    avg_annual = avgAnnual(csv_file)
    avg_daily = avgDaily(csv_file)
    daily_std_dev = dailyRetsStdev(csv_file)
    sharpe_ratio = sharpeRatio(csv_file)

    stats = {
        'stock_code': stock_code,
        'avg_annual': round(avg_annual,8),
        'avg_daily': round(avg_daily,8),
        'daily_std_dev': round(daily_std_dev,8),
        'sharpe_ratio': round(sharpe_ratio,8)
    }
    return stats
