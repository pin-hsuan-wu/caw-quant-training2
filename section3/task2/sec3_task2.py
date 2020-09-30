import talib
import numpy as np
from binance.websockets import BinanceSocketManager
from binance.client import Client
import pandas as pd

with open("./binance_api.txt") as f:
    file = f.read()
key = file.split(',')[0]
secret = file.split(',')[1]

client = Client(api_key=key, api_secret=secret)

bm = BinanceSocketManager(client)

# 1
headers = ['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime']
df = pd.DataFrame(columns=headers)


def append_df(msg):
    global df
    if msg['k']['x'] == True:
        data = pd.DataFrame({"close": [msg['k']['c']], "high": [msg['k']['h']], "low": [msg['k']['l']], "open": [
                            msg['k']['o']], "volume": [msg['k']['v']], "baseVolume": [msg['k']['q']], "datetime": [msg['E']]}, dtype=np.float64)
        data['datetime'] = pd.to_datetime(data['datetime'], unit='ms')
        data["datetime"] = data["datetime"].dt.strftime('%Y-%m-%d %H:%M:%S')
        df = df.append(data, ignore_index=True)
        output = talib.SMA(df['close'].values, timeperiod=3)
        print(output)
    else:
        pass


bm.start_kline_socket(
    'BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=append_df)
bm.start()


# 2
class Trading():

    def __init__(self):
        self.position = 0
        self.df = pd.DataFrame(columns=['close', 'high', 'low', 'open', 'volume', 'baseVolume', 'datetime'])

    def smacross(self, msg):
        if msg['k']['x'] == True:
            data = pd.DataFrame({"close": [msg['k']['c']], "high": [msg['k']['h']], "low": [msg['k']['l']], "open": [
                                msg['k']['o']], "volume": [msg['k']['v']], "baseVolume": [msg['k']['q']], "datetime": [msg['E']]}, dtype=np.float64)
            data['datetime'] = pd.to_datetime(data['datetime'], unit='ms')
            data["datetime"] = data["datetime"].dt.strftime(
                '%Y-%m-%d %H:%M:%S')
            self.df = self.df.append(data, ignore_index=True)
            sma_f = talib.SMA(self.df['close'].values, timeperiod=3)
            sma_s = talib.SMA(self.df['close'].values, timeperiod=5)
            
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

            if cross_up == True:
                self.position = 1
            if (cross_down == True) & (self.position == 1):
                self.position = 0
            print(self.position)
        else:
            pass


bm.start_kline_socket(
    'BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, callback=Trading().smacross)
bm.start()
