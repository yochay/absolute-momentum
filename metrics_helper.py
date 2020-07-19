import datetime as dt
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import style


def calc_max_drawdown(df):
    """
    Return  Daily_Drawdown and Max_Daily_Drawdown, representing DD for size of window
    Based on https://quant.stackexchange.com/questions/18094/how-can-i-calculate-the-maximum-drawdown-mdd-in-python
    """
    # We are going to use a trailing 252 trading day window
    window = 253

    # Calculate the max drawdown in the past window days for each day in the series.
    # Use min_periods=1 if you want to let the first 252 days data have an expanding window
    Roll_Max = df.rolling(window, min_periods=1).max()
    Daily_Drawdown = df / Roll_Max - 1.0

    # Next we calculate the minimum (negative) daily drawdown in that window.
    # Again, use min_periods=1 if you want to allow the expanding window
    Max_Daily_Drawdown = Daily_Drawdown.rolling(window, min_periods=1).min()
    #abs_max_DD = min(Max_Daily_Drawdown.to_list())

    #return Daily_Drawdown, Max_Daily_Drawdown
    return min(Max_Daily_Drawdown.to_list())


def calc_sharp(df):
    """
    return annualized sharp ratio 

    Nowadays, since the interest rates are so low, it is commonly assumed that the risk free rate is zero, 
    since you get very little money if you leave it in a savings account (a generic example of a risk free asset).
    """
    # daily return
    daily_return = df.pct_change(1)

    # To keep things simple, we're going to say that the risk-free rate is 0%.
    sharpe_ratio = daily_return.mean() / daily_return.std()
    annual_sharpe_ratio = math.sqrt(253) * sharpe_ratio

    return annual_sharpe_ratio


def calc_cagr(df):
    # CAGR = (1980.0/1000)**(1/6.0)-1
    """
    df representing values (use with Close of ticker or ABS_Close for algo)
    return CAGR for entire series 
    """
    # calc num of years
    total_years = len(df.index) / 253
    end_val = df.iloc[-1]
    start_val = df.iloc[0]
    cagr = (end_val / start_val) ** (1 / total_years) - 1

    return cagr


def calc_return(df):
    """
    df representing values (use with Close of ticker or ABS_Close for algo)
    return total return (performance) df[last] / df[first] 
    """
    rt = df.iloc[-1] / df.iloc[0]

    return rt


def calc_report_card(df):
    """
    calc strategy report card including total returns; CAGR; Max_DD; Sharp
    
    df represents absolute values of strategy to calculate from [0] to end [last]    
    """
    rt = calc_return(df)

    cagr = calc_cagr(df)

    sharp = calc_sharp(df)

    max_DD = calc_max_drawdown(df)

    return rt, cagr, sharp, max_DD


# testing helper functions
#data\output\SPY_ABS_a21_lb253_start_1993_01_29_end_2020_07_10.csv
#data\output\SPY_ABS_a5_lb253_start_2010_01_04_end_2020_07_10.csv
df = pd.read_csv(
    ".\\data\\output\\SPY_ABS_a21_lb253_start_1993_01_29_end_2020_07_10.csv",
    parse_dates=True,
    index_col=0,
)

print(df)

algo_type = 'Close'
df_work = df[algo_type].iloc[253:6559]
print(df_work)

#
rt, cagr, sharp, max_DD = calc_report_card(df_work)
print(f"{algo_type} report card:")
print(f"\t Return = {rt * 100}%")
print(f"\t CAGR = {cagr * 100}%")
print(f"\t Sharp = {sharp}")
print(f"\t Max DD = {max_DD * (-100)}%")


#
algo_type = 'Abs Close'
df_work = df[algo_type].iloc[253:6559]
rt, cagr, sharp, max_DD = calc_report_card(df_work)
print(f"{algo_type} report card:")
print(f"\t Return = {rt * 100}%")
print(f"\t CAGR = {cagr * 100}%")
print(f"\t Sharp = {sharp}")
print(f"\t Max DD = {max_DD * (-100)}%")


"""
plt.plot(daily_DD)
plt.plot(max_daily_DD)
plt.show()


    # Plot the results
    Daily_Drawdown.plot()
    Max_Daily_Drawdown.plot()
    plt.show()
"""

print("Done")