import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import sys
import os
from pathlib import Path
from metrics_helper import calc_report_card


# disable pandas warning 
pd.options.mode.chained_assignment = None

####### CONSTs #######

# source of data
DATA_SOURCE = 'yahoo'


# 
def download_and_save_ticker(ticker_symbol, start_date, end_date, save_folder_path):
    """ Download ticker_symble historical data between start_date and end_date from yahoo
    save ticker_symble.csv to save_folder_path 
    return DataFrame
      """
    # check if folder exists if not create it
    if(os.path.exists(Path(save_folder_path)) == False):
        os.makedirs(Path(save_folder_path))

    if(start_date > end_date):
        raise ValueError(f'start date {start_date} can not be bigger than end date {end_date}')
    else:
        try:
            df = web.DataReader(ticker_symbol, DATA_SOURCE, start_date, end_date)
            #print(df)
            file_path = f'{save_folder_path}/{ticker_symbol}.csv'
            df.to_csv(Path(file_path))
            return df
        except:
            print('something went wrong:',  sys.exc_info()[0])
        



def load_ticker(ticker_symbol, start_date, end_date, load_folder_path, refresh=False):
    """" 
    load and reutn DataFrame for a given symbole from start_date to end_date 
    download new data when refresh = True 
    download new data if file doesn't exists  
    return DataFrame
    """
    if(refresh == True):
        return download_and_save_ticker(ticker_symbol, start_date, end_date, Path(load_folder_path))
    
    
    file_path = Path(f'{load_folder_path}/{ticker_symbol}.csv')
    if(os.path.exists(file_path) == False):
        return download_and_save_ticker(ticker_symbol, start_date, end_date, Path(load_folder_path))
    

    #df = pd.read_csv( TICKERS_FOLDER + '/' + 'spy.csv')
    try:
        df = pd.read_csv( file_path)
        df.set_index("Date", inplace=True)
        df_new = df.loc[start_date:end_date]  #df_new = df.loc['2013-01-01':'2013-02-01']
        #print(df_new)
                    
        return df_new
    except (FileNotFoundError, IOError):
        print(f'could not find {ticker_symbol} symbole in {load_folder_path} folder')


# {ticker}_ABS_a{action}_lb{lookback}_start{start_date}_end{end_date}
def save_ticker(df, ticker_symbol, action, look_back, save_folder_path):
    """ save ticker to folder using naming convention"""

        # check if folder exists if not create it
    if(os.path.exists(Path(save_folder_path)) == False):
        os.makedirs(Path(save_folder_path))
    try:
        #s_date = dt.datetime.strptime(df.index[0], '%Y-%m-%d')
        start = df.index[0].strftime("%Y_%m_%d")

        #e_date = dt.datetime.strptime(df.index[len(df.index) - 1], '%Y-%m-%d')
        end  = df.index[len(df.index) - 1].strftime("%Y_%m_%d")
        ## call to save result qqq_ABS_a{action}_lb{lookback}
        file_path = f'{save_folder_path}/{ticker_symbol}_ABS_a{action}_lb{look_back}_start_{start}_end_{end}.csv'
        df.to_csv(Path(file_path))
        return True
    except (FileNotFoundError, IOError):
        print(f'could not save {ticker_symbol} symbole in {save_folder_path} folder')
        return False


def save_report_card(df, ticker_symbol, action, look_back, file_name):
    """ Append a strategy run (in df) report card to file_name
        |run date| ticker| action window | look back| start date of run| end date of run|
        then per strategy append to the same row: |return| CAGR| Max DD| Sharp|
        for Buy and Hold it looks like: | B&H return| B&H CAGR| B&H Max DD| B&H Sharp|
        for Absolute momentum: | ABS return| ABS CAGR| ABS Max DD| ABS Sharp|
    """

    # perp dates and param for creating a new report card entry
    #s_date = dt.datetime.strptime(df.index[0], '%Y-%m-%d')
    start = df.index[0].strftime("%Y_%m_%d")

    #e_date = dt.datetime.strptime(df.index[len(df.index) - 1], '%Y-%m-%d')
    end  = df.index[len(df.index) - 1].strftime("%Y_%m_%d")

    report_card_entry_header = f'{ticker_symbol}, {start}, {end}, {action}, {look_back},'

    # project Buy and Hold strategy that is represented as Close in the df
    algo_type = 'Close'
    end_index = len(df.index)
    df_work = df[algo_type].iloc[look_back:end_index]
    #print(df_work)

    #
    rt, cagr, sharp, max_DD = calc_report_card(df_work)
    rt_str = '{:6.4f}'.format(rt * 100)
    cagr_str = '{:6.4f}'.format(cagr * 100)
    sharp_str = '{:2.4f}'.format(sharp)
    max_DD_str = '{:2.4f}'.format(max_DD * (-100))

    report_card_entry_buy_n_hold = f'{rt_str}, {cagr_str}, {max_DD_str}, {sharp_str},'


    # project Absolute momentum strategy that is represented as 'Abs Close' in the df
    algo_type = 'Abs Close'
    end_index = len(df.index)
    df_work = df[algo_type].iloc[look_back:end_index]

    rt, cagr, sharp, max_DD = calc_report_card(df_work)
    rt_str = '{:6.4f}'.format(rt * 100)
    cagr_str = '{:6.4f}'.format(cagr * 100)
    sharp_str = '{:2.4f}'.format(sharp)
    max_DD_str = '{:2.4f}'.format(max_DD * (-100))

    report_card_entry_Abs = f'{rt_str}, {cagr_str}, {max_DD_str}, {sharp_str},'

    # the new line to write to the file
    report_card_entry = report_card_entry_header + report_card_entry_buy_n_hold + report_card_entry_Abs

    print(report_card_entry)
    
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        
        # If file is not empty then append '\n' for new line
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        else:
            # else write header for file 
            file_object.write("ticker, start date, end date, action time, look back window, B&H return, B&H CAGR, B&H Max DD, B&H Sharp, ABS return, ABS CAGE, ABS Max DD, ABS Sharp")
            file_object.write("\n")
        
        # Append text at the end of file
        file_object.write(report_card_entry)

    return True




"""
##### run some test

# DOWNLOAD data if needed
# start end date for data downlaod 
start = dt.datetime(1994, 1, 1)
end = dt.datetime.now()

df = download_and_save_ticker('spy', start, end, TICKERS_FOLDER)


### create report card
df = pd.read_csv(
    ".\\data\\output\\SPY_ABS_a21_lb253_start_1993_01_29_end_2020_07_10.csv",
    parse_dates=True,
    index_col=0,
)

#print(df)

file_name = ".\\data\\output\\strategies_runs.csv"

save_report_card(df, 'SPY', 21, 253, file_name)


"""
