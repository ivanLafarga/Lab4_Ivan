
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import ccxt
import pandas as pd
import numpy as np
import time


format_time= lambda x: x[:16].replace('T',' ')
current_time = lambda x : x.strftime('%Y-%m-%d %H:%M')
inner_join = lambda a,b:  pd.merge(a,b,how = 'inner', on ='TimeStamp') 
diff = lambda ts: np.diff(ts) 
roll = lambda Pt,nn: 2*(abs(np.cov(diff(Pt)[:nn],diff(Pt)[-nn-1:-1])[0,1]))**0.5 


def get_ohlc(exchanges,ticker,time_f,since,minute_limit ):
    ohlc = []
    for i in range(len(exchanges)):
      ohlc_t = pd.DataFrame(exchanges[i].fetch_ohlcv(ticker[str(exchanges[i])],time_f,since,minute_limit),columns = ['TimeStamp','open','high','close','low','Volume'])
      ohlc_t['TimeStamp'] = ohlc_t.TimeStamp.map(lambda x: format_time(ccxt.bitso.iso8601(x)))
      ohlc.append(ohlc_t)
    return ohlc

def get_ohlc_all(exchanges, tickets,time_f,since,minute_limit):
    ticker_array = []
    for ticket in tickets:
      ticker_ob = get_ohlc(exchanges,ticket,time_f,since,minute_limit )
      ticker_array.append(ticker_ob)
    return ticker_array 


def Roll(Time_S, initial_point, n_points,fixed_points):
    n = len(Time_S)
    out = np.zeros(n)
    for i in range(initial_point+1,n):
      out[i] = roll(Time_S[i-n_points-1:i],fixed_points)
    return out

def merge_all(data1,data2, exchanges, tickers, mapf,name,column, *args):

    data_f = pd.DataFrame(columns = ['Ticker', 'Exchange', 'TimeStamp','Spread', 'close'])

    for j in range(3):
      for i in range(3):
        df1 = data1[((data1.Ticker == tickers[j]) & (data1.Exchange ==exchanges[i]))]
        df2 = data2[j][i]
        df3 = inner_join(df1,df2)
        if mapf == True:
          df3[name] = Roll(df3[column],*args)
        data_f = data_f.append(df3, ignore_index = True)
    return data_f