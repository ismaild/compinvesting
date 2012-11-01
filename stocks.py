from numpy import std
from math import sqrt
from pandas import read_csv
import csv
import os

pwd = os.path.dirname(os.path.abspath(__file__))

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

def combineStocks(stock_list):
    '''
    Combines a set of stocks and returns a dict

    '''
    CSV_READER_FIELDS = ['Date','Open','High','Low', 'Close','Volume','Adj Close']
    combined_dict = {}
    cnt = 0
    for stock in stock_list:
        with open(os.path.join(pwd,'data','all',stock + '.csv'), 'r') as csvfile:
            reader = csv.DictReader(csvfile, CSV_READER_FIELDS, delimiter=',')
            reader.next()
            for row in reader:
                if cnt == 0:
                    combined_dict[row['Date']] = {}
                    combined_dict[row['Date']]['CLOSE_' + stock] = float(row['Adj Close'])
                else:
                    combined_dict[row['Date']]['CLOSE_' + stock] = float(row['Adj Close'])
        cnt += 1
    return combined_dict

def calcTotalClose(stock_dict):
    '''
    Takes in a Dict of stock values per a day, and returns a new dict with the total of the adjusted close
    '''
    stock_dict = stock_dict.copy()
    for day in stock_dict:
        #print day, stock_dict[day].keys(), stock_dict[day]
        stock_total = 0.0
        for key in stock_dict[day].keys():
            #print stock_dict[day][key]
            stock_total += stock_dict[day][key]
        stock_dict[day]['Adj Close'] = stock_total
    #print stock_dict
    return stock_dict

def writeCombinedStocks(stock_list, output_name):
    '''
    Writes the combined stock to csv

    Takes a list of stocks, and output name
    '''
    c_stocks = combineStocks(stock_list)
    ct_stocks = calcTotalClose(c_stocks)
    #print ct_stocks
    with open(os.path.join(pwd,'data',output_name + '.csv'), 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        header = []
        header.append('Date')
        for stock in stock_list:
            header.append('CLOSE_' + stock)
        header.append('Adj Close')
        writer.writerow(header)
        for key in sorted(ct_stocks.keys()):
            #writer.writerow('a')
            row = [key]
            for stock in stock_list:
                row.append(ct_stocks[key]['CLOSE_' + stock])
            row.append(ct_stocks[key]['Adj Close'])
            #print row
            writer.writerow(row)