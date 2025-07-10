import pandas as pd
#binance
from binance import Client
#Date
from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
#json
import json

class data_crypto:
    
    def __init__(self):
        with open(r'C:\Users\dylan\OneDrive\Documentos\Git\Codes\Cryptos\Credentials\binance_credentials.json', 'r') as fp:
            access_params = json.load(fp)
        #assert "crypto" in access_params.keys(), "access_params must have a crypto"
        #assert "days_back" in access_params.keys(), "consumer_secret must have a days_back"
        #assert "time" in access_params.keys(), "access_token must have a time"
        assert "api_key" in access_params.keys(), "access_token_secret must have a api_key"
        assert "api_secret" in access_params.keys(), "access_token_secret must have a api_secret"
        #self.crypto = access_params["crypto"]
        #self.days_back = access_params["days_back"]
        #self.time = access_params["time"]
        self.api_key = access_params["api_key"]
        self.api_secret = access_params["api_secret"]
        
    def crypto_download(self, params):
        #crypto = input('Nombre de la cryptomoneda: ').upper()
        try:
            if params['time'].upper() == '1YEAR':
                interval = Client.KLINE_INTERVAL_1YEAR
            elif params['time'].upper() == '1MONTH':
                interval = Client.KLINE_INTERVAL_1MONTH
            elif params['time'].upper() == '1WEEK':
                interval = Client.KLINE_INTERVAL_1WEEK
            elif params['time'].upper() == '1DAY':
                interval = Client.KLINE_INTERVAL_1DAY
            elif params['time'].upper() == '1HOUR':
                interval = Client.KLINE_INTERVAL_1HOUR
            elif params['time'].upper() == '1MINUTE':
                interval = Client.KLINE_INTERVAL_1MINUTE
            elif params['time'].upper() == '15MINUTE':
                interval = Client.KLINE_INTERVAL_15MINUTE
        except:
            print('WRONG TIME: 1YEAR, 1MONTH, 1WEEK, 1DAY, 1HOUR, 1MINUTE, 15MINUTE')
        ################################################Binance Api################################################
        client = Client(self.api_key, self.api_secret)
        converter = 'USDT'
        crypto_symbol = f"{params['crypto']}USDT"
        #interval = Client.KLINE_INTERVAL_1DAY
        #date_back = dt.timedelta(days=1)

        #Simbolos disponibles
        symbol = pd.DataFrame(client.get_all_tickers())
        symbol = symbol[symbol['symbol'].str.endswith(converter)]['symbol'].replace(converter, '', regex=True).sort_values().reset_index(drop=True)

        #Traigo data de la crypto seteada
        klines = client.get_historical_klines(crypto_symbol, interval, 
                                           pd.to_datetime(datetime.now() - relativedelta(days = params['days_back'])).strftime('%d %b, %Y'),
                                              (datetime.now() + dt.timedelta(days=1)).strftime('%d %b, %Y'))
        c_data = pd.DataFrame(klines)
        date = []
        for i in c_data[0]:
            date.append(pd.to_datetime(dt.datetime.fromtimestamp(i/1000).strftime("%Y-%m-%d %H:%M:%S")))
        c_data[0] = date
        c_data = c_data[[0,1,2,3,4,5,7]]
        c_data.rename(columns={0:'Date', 1:'Open', 2:'High', 3:'Low', 4:'Close', 5:'Volumen', 7:'Volumen USD'}, inplace=True)
        c_data.set_index('Date', inplace=True)
        for i in c_data.columns:
            c_data[i] = c_data[i].astype('float64')

        c_data.reset_index(inplace=True)
        return(c_data)