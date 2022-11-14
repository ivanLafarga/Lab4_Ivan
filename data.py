
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import functions as fun
import numpy as np
import ccxt
import warnings
import pandas as pd
warnings.filterwarnings("ignore")


bitmart = ccxt.bitmart()
gateio = ccxt.gateio()
bitget = ccxt.bitget()
exa = [bitmart, gateio, bitget] 


limit = 30

from_datime = '2022-11-14T06:08:11.000Z' 
since = bitmart.parse8601(from_datime) 

dic_btc = {str(bitmart):'BTC/USDT',str(gateio):'BTC/USDT',str(bitget):'BTC/USDT'}
dic_bnb = {str(bitmart):'BNB/USDT',str(gateio):'BNB/USDT',str(bitget):'BNB/USDT'}
dic_doge = {str(bitmart):'DOGE/USDT',str(gateio):'DOGE/USDT',str(bitget):'DOGE/USDT'}

df = pd.read_csv(r'files/DATOS_Limpios.csv')

ohlc = fun.get_ohlc_all(exa,[dic_btc, dic_bnb, dic_doge],'1m',since,94)

spread_data = fun.merge_all(df,ohlc,[str(bitmart),str(gateio),str(bitget)],['BTC/USDT','BNB/USDT','DODGE/USDT'],
                                True,'Effective Spread','close',11,11,5)
