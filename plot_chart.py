
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web


rcParams['figure.figsize'] = (16,8)
style.use('ggplot')

df = pd.read_csv('.\\data\\output\\SPY_ABS_a5_lb253.csv', parse_dates=True, index_col=0)

print(df)

df['100ma'] = df['Close'].rolling(100).mean()
df['200ma'] = df['Close'].rolling(200).mean()


print(df)


ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)

ax1.plot(df.index, df['Close'])
ax1.plot(df.index, df['Abs Close'])
ax1.plot(df.index, df['200ma'])
#ax2.bar(df.index, df['Volume'])

plt.show()

print('Done')