import pandas as pd
import numpy as np
import requests
import calendar
from datetime import timedelta, date

def third_wednesday(d, n):
    """Given a date, calculates n next third fridays
   https://stackoverflow.com/questions/28680896/how-can-i-get-the-3rd-friday-of-a-month-in-python/28681097"""
 
    def next_third_wednesday(d):
        d += timedelta(weeks=4)
        return d if d.day >= 15 else d + timedelta(weeks=1)
 
    # Find closest wednesday to 15th of month
    s = date(d.year, d.month, 21)
    result = [s + timedelta(days=(calendar.WEDNESDAY - s.weekday()) % 7)]
 
    # This month's third wednesday passed. Find next.
    if result[0] < d:
        result[0] = next_third_wednesday(result[0])
 
    for i in range(n - 1):
        result.append(next_third_wednesday(result[-1]))
 
    return result

def download():
    for d in third_wednesday(date(2013, 1, 1), 8*12):
        s = "{}-{}-{}".format(d.year, d.month, d.day)
        r = requests.get("https://markets.cboe.com/us/futures/market_statistics/historical_data/products/csv/VX/{}".format(s))

        with open(s + '.csv', 'w+') as f:
            f.write(r.text)

df = pd.DataFrame()

for d in third_wednesday(date(2013, 1, 1), 8*12):
    csv = pd.read_csv("{}-{}-{}.csv".format(d.year, d.month, d.day))
    n = csv['Futures'][0]
    csv = csv.rename(columns={'Close': n})
    if len(df) == 0:
        df = csv[['Trade Date', n]]
    else:
        df = df.merge(csv[['Trade Date', n]], how='outer', on='Trade Date')

df.fillna(0, inplace='true')
df.to_csv('df.csv')

data = df.values.tolist()

with open('cleaned.csv', 'w+') as f:
    f.write(','.join(['Trade Date'] + ['F{}'.format(x) for x in range(1, 10)]) + '\n')
    for row in data[1:]:
        f.write(','.join([str(x) for x in row if x != 0.0]) + '\n')
