import krakenex
from pykrakenapi import KrakenAPI
import pandas as pd
import time
from datetime import datetime
from pymongo_get_database import get_database
from collections import ChainMap

#kraken API information
api = krakenex.API(<krakenAPI>)
k = KrakenAPI(api)

#retrieving BTC OLHC
ohlc = k.get_ohlc_data('BTCUSD', interval=60, ascending = False)

#converting to dataframe to manipulate data
df = pd.DataFrame(ohlc[0],columns = ['time','open','high','low','close','vwap','volume','count'])
df.index = df.index.date
date_time_begin = datetime(2024, 1, 1, 12, 0, 0)  # Year, Month, Day, Hour, Minute, Second
date_time_end = datetime(2024, 8, 19, 12, 0, 0)
timestamp_begin = int(time.mktime(date_time_begin.timetuple()))
timestamp_end = int(time.mktime(date_time_end.timetuple()))

#transform data
filtered_df = df[(df['time'] >= timestamp_begin) & (df['time'] <= timestamp_end)]
filtered_df = filtered_df.reset_index(drop=True)
filtered_df['timestamp'] = pd.to_datetime(filtered_df['time'],unit = 's')

#convert to dict to input in MongoDB
btc = filtered_df.to_dict(orient='records')
btc = {str(item['time']): item for item in btc} #use as index



#insert data in MongoDB
dbname = get_database()
collection_name = dbname["btc"]
for i in btc:
    #print(btc[i])
    collection_name.insert_many([btc[i]])
