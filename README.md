# kraken project

A simple project to showcase BTCUSD maximum close values in a specific period of time.

## 1. Connecting with Kraken API and retrieving data

The insert.py code starts by connecting with Kraken and retrieving BTCUSD values OLHC hourly

```
api = krakenex.API("<KrakenAPI>")
k = KrakenAPI(api)

ohlc = k.get_ohlc_data('BTCUSD', interval=60, ascending = False)
```
Next, the information is converted to a DataFrame to be manipulated with Pandas.
The code for the time is converted to timestamp for a better understanding using ```datetime```.

```
df = pd.DataFrame(ohlc[0],columns = ['time','open','high','low','close','vwap','volume','count'])
df.index = df.index.date
date_time_begin = datetime(2024, 1, 1, 12, 0, 0)  # Year, Month, Day, Hour, Minute, Second
date_time_end = datetime(2024, 8, 19, 12, 0, 0)
timestamp_begin = int(time.mktime(date_time_begin.timetuple()))
timestamp_end = int(time.mktime(date_time_end.timetuple()))
```

We assign a filter from 01.01.2024 to 19.08.2024 and filter the data 
```
filtered_df = df[(df['time'] >= timestamp_begin) & (df['time'] <= timestamp_end)]
filtered_df = filtered_df.reset_index(drop=True)
filtered_df['timestamp'] = pd.to_datetime(filtered_df['time'],unit = 's')
```
After that, the data in converted to a dictionary so it can input in our MongoDB database.

```
btc = filtered_df.to_dict(orient='records')
btc = {str(item['time']): item for item in btc} #use as index
```

## Inserting information in the MongoDB database

The connection is stablished to MongoDB in ```pymongo_get_database.py```

```
from pymongo import MongoClient

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "<MongoDB API>"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['kraken']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()

```

With this, back in the ```insert.py```, the retrieved data is inserted by
```
dbname = get_database()
collection_name = dbname["btc"]
for i in btc:
    #print(btc[i])
    collection_name.insert_many([btc[i]])
```

With that, the filtered desired information is retrieved from Kraken and stored in MongoDB.

![image](https://github.com/user-attachments/assets/0918999d-2072-47ca-bd73-edb032f4610c)


## Read from MongoDB and analyze data

The ```retrieve.py``` code shows how to read from MongoDB.
```
#connect to db
dbname = get_database()
collection_name = dbname["btc"]

#retrieve the BTC database
db = collection_name.find()
df = pd.DataFrame(list(db))
```

Using Pandas again to manipulate only the necessary data to analyze, we filter only for August 2024 data.
```
#manipulate and filter data
filtered_df = df[df['timestamp'] >= '2024-08-01'] 
filtered_df['date'] = pd.to_datetime(filtered_df['timestamp']).dt.date
```
Since the granularity is timestamp, it is necessary to convert timestamp to datetime. Next, we aggregate by day and choose only the maximum Close value of each day.
```
group = filtered_df.groupby('date')['close'].max().reset_index()
```

## Plot Result

```

fig, ax1 = plt.subplots()
ax1.set_xlabel('date')
ax1.set_xticklabels(group['date'], rotation= 90)
ax1.set_ylabel('close',color = 'tab:red')
ax1.plot(group['date'], group['close'])
ax1.tick_params(axis = 'y')
fig.tight_layout()
plt.show()

```

![image](https://github.com/user-attachments/assets/ff708fad-91e9-4aa0-a6c4-a82c5593af48)

