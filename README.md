# krakenproject

A simple project to showcase BTCUSD maximum close values in a specific period of time.

## 1. Connecting with Kraken API and retrieving data

The insert.py code starts by connecting with Kraken and retrieving BTCUSD values OLHC hourly

'api = krakenex.API("<KrakenAPI>")
k = KrakenAPI(api)'

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
