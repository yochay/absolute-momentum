
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
from matplotlib import style
from symbols import load_ticker, save_ticker
from algorithm import calc_absolute_momentum


# disable pandas warning 
pd.options.mode.chained_assignment = None

####### CONSTs #######

# folders
TICKERS_FOLDER = '.\\data\\tickers'     # tickers folder
OUTPUT_FOLDER = '.\\data\\output'       # result folder 


##### values for algo ###### 

action = 5      # how often do we evaluate and 'take' action
lookback = 253   # what is te lookback duration 
ticker = 'SPY'   # the ticker

# dates to back test
start_date = '1995-01-01'  
end_date = dt.datetime.now().strftime('%Y-%m-%d') 

# read from csv
df = load_ticker(ticker, start_date, end_date, TICKERS_FOLDER, False)
print(df)

df_res = calc_absolute_momentum(df, action, lookback)
print(df_res)

save_ticker(df_res, ticker, action, lookback, OUTPUT_FOLDER)

# for Numpy and matplotlib sytle 
""" style.use('ggplot')

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)

ax1.plot(df_res.index, df_res['Close'])
ax1.plot(df_res.index, df_res['Abs Close'])
#ax2.bar(df.index, df['Volume'])

plt.show()
 """
""" 
fig = plt.figure()
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
ax1.xaxis_date()
 """