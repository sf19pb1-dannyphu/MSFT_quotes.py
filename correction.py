"""
MSFT_quotes.py

Reads JSON file and prints today's, yesterday's and avg stock prices for MSFT.
"""

import sys
import urllib.parse
import urllib.request
import json
import datetime
import statistics
import pandas as pd

query = {
    "apikey":   "demo",
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol":   "MSFT"   #Microsoft
}

params = urllib.parse.urlencode(query)
url = f"https://www.alphavantage.co/query?{params}"

#Read in JSON file
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

try:
    dailyDict = bigDictionary['Time Series (Daily)']
except KeyError as error:
    print(error, file = sys.stderr)
    sys.exit(1)

#Get the two most recent dates in the time series.

dates = dailyDict.keys()
dates = sorted(dates, key = lambda d: datetime.datetime.strptime(d, "%Y-%m-%d")) #chronological order
today = dates[-1]   #The latest date is at the very end.
yest  = dates[-2]   #Next-to-latest date.  Can combine to yest, today = dates[-2:]

"""
#Stock market is open only weekdays. Another way to do dates.

if tod.weekday() == 0:  #if today is Monday
    days = 3            #go back 3 days to the previous Friday
else:
    days = 1

delta = datetime.timedelta(days = days)
yest = (tod - delta).strftime("%Y-%m-%d")
"""




#Compute the average high and low using Python.

hiList = [float(value["2. high"]) for value in dailyDict.values()]
loList = [float(value["3. low"])  for value in dailyDict.values()]

hiAvg = statistics.mean(hiList)
loAvg = statistics.mean(loList)

print(f"hiAvg = $ {hiAvg:.4f}")
print(f"loAvg = $ {loAvg:.4f}")
print()

#Compute the average high and low using pandas.

df = pd.DataFrame(dailyDict)

avg_hi = df.loc['2. high'].astype(float).mean()
avg_lo = df.loc['3. low' ].astype(float).mean()

print("Microsoft (MSFT) High/Low:")
print()

#TODAY'S PRICES
print(f"today = {today}")
todaysPrices = dailyDict[today]
print(f'Today\'s High:    $ {todaysPrices["2. high"]}')
print(f'Today\'s Low:     $ {todaysPrices["3. low"]}')
print()

#Previous Day's PRICES
print(f"yesterday = {yest}")
yesterdaysPrices = dailyDict[yest]
print(f'Prev Day\'s High: $ {yesterdaysPrices["2. high"]}')
print(f'Prev Day\'s Low:  $ {yesterdaysPrices["3. low"]}')
print()

#Average high/low from entire JSON file: includes roughly ~40 weekdays or 2 months
print(f'2 Mo. High Avg:  $ {avg_hi:.4f}')
print(f'2 Mo. Low Avg:   $ {avg_lo:.4f}')

#Tried to do a 30 day average instead of the whole JSON file but too advanced, couldn't figure it out
#print(f'30 day High Avg: $ {hiAvg:.4f}')
#print(f'30 day Low Avg:  $ {loAvg:.4f}')

sys.exit(0)
