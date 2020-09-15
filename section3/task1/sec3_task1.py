from binance.websockets import BinanceSocketManager
from binance.client import Client
import pandas as pd
import datetime

with open("./binance_api.txt") as f:
    file = f.read()
key = file.split(',')[0]
secret = file.split(',')[1]

client = Client(api_key= key,api_secret= secret)

bm = BinanceSocketManager(client)

#1.
def process_message(msg):
    print(msg)

bm.start_kline_socket('BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=process_message)
bm.start()

#2.
def append_df(msg):
    headers = ['close' ,'high' ,'low','open','volume','baseVolume','datetime','x']    
    df = pd.DataFrame(columns=headers)
    data = pd.DataFrame({"close": [msg['k']['c']],"high": [msg['k']['h']],"low": [msg['k']['l']],"open": [msg['k']['o']],"volume": [msg['k']['v']],"baseVolume": [msg['k']['q']],"datetime": [msg['E']], "x": [msg['k']['x']]})
    df = df.append(data, ignore_index=True)
    df["datetime"] = pd.to_datetime(df['datetime'], unit = 'ms')
    df["datetime"] = df["datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
    if msg['k']['x'] == True:
        print(df)
    else:
        pass

bm.start_kline_socket('BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=append_df)
bm.start()

#3.
def csv_df(msg):
    headers = ['close' ,'high' ,'low','open','volume','baseVolume','datetime','x']    
    df = pd.DataFrame(columns=headers)
    if msg['k']['x'] == True:
        data = pd.DataFrame({"close": [msg['k']['c']],"high": [msg['k']['h']],"low": [msg['k']['l']],"open": [msg['k']['o']],"volume": [msg['k']['v']],"baseVolume": [msg['k']['q']],"datetime": [msg['E']], "x": [msg['k']['x']]})
        df = df.append(data, ignore_index=True)
        df["datetime"] = pd.to_datetime(df['datetime'], unit = 'ms')
        df["datetime"] = df["datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.to_csv('BTCUSDT.csv')
    else:
        pass

bm.start_kline_socket('BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=csv_df)
bm.start()