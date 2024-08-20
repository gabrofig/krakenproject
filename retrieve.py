import pymongo
from pymongo_get_database import get_database
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


#connect to db
dbname = get_database()
collection_name = dbname["btc"]

#retrieve the BTC database
db = collection_name.find()
df = pd.DataFrame(list(db))

#manipulate and filter data
filtered_df = df[df['timestamp'] >= '2024-08-01'] 
filtered_df['date'] = pd.to_datetime(filtered_df['timestamp']).dt.date

group = filtered_df.groupby('date')['close'].max().reset_index()

#plot close data 

fig, ax1 = plt.subplots()
ax1.set_xlabel('date')
ax1.set_xticklabels(group['date'], rotation= 90)
ax1.set_ylabel('close',color = 'tab:red')
ax1.plot(group['date'], group['close'])
ax1.tick_params(axis = 'y')
fig.tight_layout()
plt.show()
