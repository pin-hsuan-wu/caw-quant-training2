import talib
import numpy as np
from binance.websockets import BinanceSocketManager
from binance.client import Client
import pandas as pd

with open("./binance_api.txt") as f:
    file = f.read()
key = file.split(',')[0]
secret = file.split(',')[1]

client = Client(api_key= key,api_secret= secret)

bm = BinanceSocketManager(client)
 
#1
headers = ['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime']    
df = pd.DataFrame(columns=headers)

def append_df(msg):
    global df
    if msg['k']['x'] == True:
        data = pd.DataFrame({"close": [msg['k']['c']],"high": [msg['k']['h']],"low": [msg['k']['l']],"open": [msg['k']['o']],"volume": [msg['k']['v']],"baseVolume": [msg['k']['q']],"datetime": [msg['E']]}, dtype=np.float64)
        data['datetime'] = pd.to_datetime(data['datetime'], unit = 'ms')
        data["datetime"] = data["datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
        df = df.append(data, ignore_index=True)
        output = talib.SMA(df['close'].values, timeperiod=3)
        print(output)    
    else:
        pass

bm.start_kline_socket('BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=append_df)
bm.start()


#2
headers = ['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime']    
df = pd.DataFrame(columns=headers)

class trading():

    def __init__(self):
        self.position = 'xxx'
    def smacross(self, msg):
        global df
        if msg['k']['x'] == True:
            data = pd.DataFrame({"close": [msg['k']['c']],"high": [msg['k']['h']],"low": [msg['k']['l']],"open": [msg['k']['o']],"volume": [msg['k']['v']],"baseVolume": [msg['k']['q']],"datetime": [msg['E']]}, dtype=np.float64)
            data['datetime'] = pd.to_datetime(data['datetime'], unit = 'ms')
            data["datetime"] = data["datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
            df = df.append(data, ignore_index=True)
            sma_f = talib.SMA(df['close'].values, timeperiod=3)
            sma_s = talib.SMA(df['close'].values, timeperiod=5) 
        else:
            pass
    def cross_up(self, sma_f, sma_s):
        if sma_f[-1] > sma_s[-1]:
            return True
        else:
            return False
    def cross_down(self, sma_f, sma_s):
        if sma_f[-1] < sma_s[-1]:
            return True
        else:
            return False


bm.start_kline_socket('BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=trading.smacross)
bm.start()