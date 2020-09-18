from binance.websockets import BinanceSocketManager
from binance.client import Client
import pandas as pd

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
headers = ['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime']    
df = pd.DataFrame(columns=headers)

def append_df(msg):
    global df
    if msg['k']['x'] == True:
        data = pd.DataFrame({"close": [msg['k']['c']],"high": [msg['k']['h']],"low": [msg['k']['l']],"open": [msg['k']['o']],"volume": [msg['k']['v']],"baseVolume": [msg['k']['q']],"datetime": [msg['E']]})
        data['datetime'] = pd.to_datetime(data['datetime'], unit = 'ms')
        data["datetime"] = data["datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
        df = df.append(data, ignore_index=True)
        print(df)
    else:
        pass

bm.start_kline_socket('BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=append_df)
bm.start()


#3.
headers = ['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime']   
df = pd.DataFrame(columns=headers)
df.to_csv('BTCUSDT.csv')

def csv_df(msg):
    global df
    while msg['k']['x'] == True:
        data = pd.DataFrame({"close": [msg['k']['c']],"high": [msg['k']['h']],"low": [msg['k']['l']],"open": [msg['k']['o']],"volume": [msg['k']['v']],"baseVolume": [msg['k']['q']],"datetime": [msg['E']]})
        data['datetime'] = pd.to_datetime(data['datetime'], unit = 'ms')
        data["datetime"] = data["datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
        df = df.append(data, ignore_index=True)
        with open('BTCUSDT.csv', 'a') as f:
            df.tail(1).to_csv(f, header=False)
        break
    else:
        pass

bm.start_kline_socket('BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=csv_df)
bm.start()