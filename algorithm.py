
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
from matplotlib import style
from symbols import load_ticker, save_ticker


# disable pandas warning 
pd.options.mode.chained_assignment = None


###### Absolute MOMENTUM #######


###### HELPER FUNCTIONS #######
#
def get_action_window_days (action_start, action_size, max_trading_days):
    """ make sure that we do not run out of index during scane 
        return the action window size (numnber of day between actions)
    """
    ret_val = action_start + action_size
    if (ret_val > max_trading_days):
        ret_val = max_trading_days
    return ret_val


# helpers for running algorithem
RISK_ON = True
RISK_OFF = False


# ABS ALGO
def calc_absolute_momentum(df, action, lookback):
    """ Calculate absolute momentum 
        more info TBD
    """
    ###### prep data for algo ######
    # create a copy df to work with
    df_work = df[['Adj Close']]
    df_work.rename(columns = {'Adj Close':'Close'}, inplace = True)

    # calc daily return compare to self (daily return = 1- val[i]/val[i-1])
    df_work['Daily return'] =  df_work['Close'].pct_change(1)
    # calc absolute value starting $1   
    df_work['Ticker returns'] =  (1 + df_work['Daily return']).cumprod()
    print(df_work)

    # calc lookback window return daily (lookback return) = 1- val[i]/ val[i-lookback]
    df_work['lookback window'] =  df_work['Close'].pct_change(lookback)  

    # Abs close represent close value following the algo RISK signals,  
    # RISK ON AbsClose[i] = AbsClose[i] * (1 + daily[i-1])
    # RISK OFF AbsClose[i] = last AbsCLose before swtich to RISKOFF
    df_work['Abs Close'] =  ''
    # identifys absolute regim, risk ON/ OFF, easier to debug
    df_work['RISK'] =  ''
    # profit or call per change in transaction
    df_work['PROFIT'] =  ''
    # profit or call per change in transaction
    df_work['EOY_PROFIT'] =  ''

    print(df_work)

    # set up params
    # total number of trading days to analyze, length of the df, assuming entire df has trading info
    total_trading_days = len(df_work.index)

    # default to RISK_ON to handle case of RISK_OFF as the first iteration of the algo run
    risk_status = RISK_ON

    # set the start value of Abs Close to the first day we can test, which is the of the lookback window size
    start_close_value = df_work.iloc[lookback-1]['Close']

    # we use close_price_to_copy to save the last value of RISK ON for duration of risk off time...
    close_price_to_copy = -1
    
    # we need to keep the price we bought the stock at to calculate profit and lost.
    last_bought_at = start_close_value

    #aggrigate the profit and lost on a yealy basis
    yearly_aggrigated_profit = 0

    df_work['Abs Close'].iloc[lookback-1] = start_close_value

    print(f'start algo run from {lookback} until {total_trading_days}')
    #counter = 1

    for action_day in range(lookback, total_trading_days, action):
        # print to see if algo is running         

        # Calc profit 
        # compare if next trading day is new year, lock down total aggregate for year for tax calc
        #t1 = str(df_work.index[action_day])[0:4]
        #t2 = str(df_work.index[action_day+1])[0:4]
        if((action_day+1) < len(df_work.index) and  str(df_work.index[action_day])[0:4] != str(df_work.index[action_day+1])[0:4] ):
            #time to calculate yearly profit for tax
            df_work['EOY_PROFIT'].iloc[action_day] = yearly_aggrigated_profit
            yearly_aggrigated_profit = 0

        # reset risk_change each time we evaluate 
        risk_change = False
        # Risk on/off assesment based on lookback window to establish absolute strangth 
        if ( df_work['lookback window'].iloc[action_day] > 0 ):
            #print("RISK ON")

            # RISK Change - from OFF to ON
            if(risk_status == RISK_OFF):
                risk_change = True

                # Calc profit - we are going to buy stock, need to set profit baseline
                last_bought_at = df_work.iloc[action_day-1]["Abs Close"] * (1 + df_work.iloc[action_day]["Daily return"])
                #since we buy in at end of day. When returning from RISK OFF, we need to have one more day of last closed value 
                #df_work.iloc[action_day] = close_price_to_copy # we are going to skip one day when returning from RISK OFF
                #[TODO: when returning from RISK, we need special case the frist day. Need to copy last abs close and have a shorter sycle - of one day]

            risk_status = RISK_ON
            df_work['RISK'].iloc[action_day] = "RISK ON"

            #make sure we dont run out of index at the end of run. action_windows_days_end holds the current day + lookback window
            action_window_days_end = get_action_window_days(action_day, action, total_trading_days)
            #copy for durtion of action
            for day in range(action_day, action_window_days_end):
                # handle risk change (only when change from OFF to --> ON)
                if(risk_change == True):
                    # print(' RISK CHANGE')
                    risk_change = False # reset the flag so we track risk change only one time
                    # since we buy at end of day or on next open, for the day we move from risk OFF to ON, we copy the RISK off value one more day
                    # close_price_to_copy >0 means we run through a cycle of ON to OFF before at least once
                    if(close_price_to_copy > 0 ):
                        df_work['Abs Close'].iloc[day] = close_price_to_copy
                    else:
                        # algo stared with off --> (this code should be unreachable? )
                        df_work['Abs Close'].iloc[day] =  start_close_value
                else:
                    new_abs_close = df_work.iloc[day-1]["Abs Close"] * (1 + df_work.iloc[day]["Daily return"])
                    df_work['Abs Close'].iloc[day] = new_abs_close  #df_work.iloc[day,2] = close #df_work.iloc[day]["Close"] 
                    #print(df_work.iloc[day][["Close", 'Abs Close']])
        
        else:
            #print("RISK OFF")
            # if we ditect a regim change, we copy value of prev day and keep it flat. 
            # if risk_status is already OFF, then do change the last close price to copy
            df_work['RISK'].iloc[action_day] = "RISK OFF"
            if(risk_status == RISK_ON):
                risk_status = RISK_OFF
                #close_price_to_copy = df_work.iloc[action_day-1]["Abs Close"]  # copy the value from the previos day and use that
                close_price_to_copy = df_work.iloc[action_day-1]["Abs Close"] * (1 + df_work.iloc[action_day]["Daily return"])
                df_work['PROFIT'].iloc[action_day] = close_price_to_copy  - last_bought_at
                yearly_aggrigated_profit += df_work['PROFIT'].iloc[action_day]

            #make sure we dont run out of index
            action_window_days_end = get_action_window_days(action_day, action, total_trading_days)
            for day in range(action_day, action_window_days_end):
                df_work['Abs Close'].iloc[day] = close_price_to_copy
                #print(df_work.iloc[day][["Close", 'Abs Close']])

    return df_work