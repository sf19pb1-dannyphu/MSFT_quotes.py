"""
MSFT_quotes.py

Reads JSON file and print's today's, Yesterday's and avg stock prices for MSFT.
"""

import sys
import urllib.request
import json
import datetime
import statistics
import pandas as pd

url = "https://www.alphavantage.co/query?apikey=demo&function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT"

#Read in Json file
try:
    infile = urllib.request.urlopen(url)
except urllib.error.URLError as error:
    print(error, file = sys.stderr)
    sys.exit(1)

sequenceOfBytes = infile.read()         #Read the entire input file.
infile.close()

try:
    s = sequenceOfBytes.decode("utf-8") #s is a string.
except UnicodeError as error:
    print(error, file = sys.stderr)
    sys.exit(1)

try:
    bigDictionary = json.loads(s)          #bigDictionary is a dict
except json.JSONDecodeError as error:
    print(error, file = sys.stderr)
    sys.exit(1)

#Datetime section
today = datetime.datetime.today().strftime("%Y-%m-%d")

tod = datetime.date.today()

#stock market is only open on weekdays
if (tod - datetime.timedelta(days = 1)).weekday() < 5:
    yest = (tod - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
else:
    yest = (tod - datetime.timedelta(days = 3)).strftime("%Y-%m-%d")



#Average section - cant get commented part below to work correctly without using pandas :(

"""
#for i in bigDictionary['Time Series (Daily)'].keys():
    hiList = [float(bigDictionary['Time Series (Daily)'][0]['2. high'])]
    loList = [float(bigDictionary['Time Series (Daily)'][0]['3. low'])]
    
# ? Lines below prints correctly! but can't get all values into the variable
#for i in bigDictionary['Time Series (Daily)'].keys():   
    #print(bigDictionary['Time Series (Daily)'][i]['2. high']) 

hiAvg = statistics.mean(hiList)
loAvg = statistics.mean(loList)
"""

#got it to work using pandas but still would like to see it done without using pandas

df = pd.DataFrame(bigDictionary['Time Series (Daily)'])

avg_hi = df.loc['2. high',:].apply(lambda x: float(x)).mean()
avg_lo = df.loc['3. low',:].apply(lambda x: float(x)).mean()


print("Microsoft (MSFT) High/Low:")

print()#TODAY'S PRICES
print(f'Today\'s High:    $ {bigDictionary["Time Series (Daily)"][today]["2. high"]}')
print(f'Today\'s Low:     $ {bigDictionary["Time Series (Daily)"][today]["3. low"]}')

print() #Previous Day's PRICES
print(f'Prev Day\'s High: $ {bigDictionary["Time Series (Daily)"][yest]["2. high"]}')
print(f'Prev Day\'s Low:  $ {bigDictionary["Time Series (Daily)"][yest]["3. low"]}')

print()
#Average high/low from entire JSON file: includes roughly ~40 weekdays or 2 months
print(f'2 Mo. High Avg:  $ {avg_hi:.4f}')
print(f'2 Mo. Low Avg:   $ {avg_lo:.4f}')



#Tried to do a 30 day average instead of the whole JSON file but too advanced, couldnt figure it out
#print(f'30 day High Avg: $ {hiAvg:.4f}')
#print(f'30 day Low Avg:   $ {loAvg:.4f}')
