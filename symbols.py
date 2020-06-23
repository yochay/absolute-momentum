import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import sys
import os


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
    if(os.path.exists(save_folder_path) == False):
        os.makedirs(save_folder_path)

    if(start_date > end_date):
        raise ValueError(f'start date {start_date} can not be bigger than end date {end_date}')
    else:
        try:
            df = web.DataReader(ticker_symbol, DATA_SOURCE, start_date, end_date)
            #print(df)
            file_path = f'{save_folder_path}/{ticker_symbol}.csv'
            df.to_csv(file_path)
        except:
            print('something went wrong:',  sys.exc_info()[0])
        return df



def load_ticker(ticker_symbol, start_date, end_date, load_folder_path, refresh=False):
    """" 
    load and reutn DataFrame for a given symbole from start_date to end_date 
    download new data when refresh = True 
    download new data if file doesn't exists  
    return DataFrame
    """
    if(refresh == True):
        return download_and_save_ticker(ticker_symbol, start_date, end_date, load_folder_path)
    
    
    file_path = f'{load_folder_path}/{ticker_symbol}.csv'
    if(os.path.exists(file_path) == False):
        return download_and_save_ticker(ticker_symbol, start_date, end_date, load_folder_path)
    

    #df = pd.read_csv( TICKERS_FOLDER + '/' + 'spy.csv')
    try:
        df = pd.read_csv( f'{load_folder_path}/{ticker_symbol}.csv')
        df.set_index("Date", inplace=True)
        df_new = df.loc[start_date:end_date]  #df_new = df.loc['2013-01-01':'2013-02-01']
        #print(df_new)
                    
        return df_new
    except (FileNotFoundError, IOError):
        print(f'could not find {ticker_symbol} symbole in {load_folder_path} folder')


#
def save_ticker(df, ticker_symbol, action, look_back, save_folder_path):
    """ save ticker to folder using naming convention"""

        # check if folder exists if not create it
    if(os.path.exists(save_folder_path) == False):
        os.makedirs(save_folder_path)
    try:
        #OUTPUT_FOLDER
        ## call to save result qqq_ABS_a{action}_lb{lookback}
        file_path = f'{save_folder_path}/{ticker_symbol}_ABS_a{action}_lb{look_back}.csv'
        df.to_csv(file_path)
        return True
    except (FileNotFoundError, IOError):
        print(f'could not save {ticker_symbol} symbole in {save_folder_path} folder')
        return False




"""  
# DOWNLOAD data if needed
# start end date for data downlaod 
start = dt.datetime(1994, 1, 1)
end = dt.datetime.now()

df = download_and_save_ticker('spy', start, end, TICKERS_FOLDER)

 """
