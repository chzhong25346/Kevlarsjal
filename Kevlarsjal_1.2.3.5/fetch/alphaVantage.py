import pandas as pd
import sys
import logging
import json
from datetime import datetime as dt
from alpha_vantage.timeseries import TimeSeries
logger = logging.getLogger('main.alphaVantage')

def get_av(ticker,size='compact',today_only=False,intraday='30min'):
    """
    size= compact or full, return df
    """
    try:
        ts = TimeSeries(key='6E970DLNQ4GZJDRF',indexing_type='date')
        if (intraday == 'none'):
            return get_daily_adjusted(ticker,ts,size,today_only)
        elif(intraday != 'none'):
            return get_intraday(ticker,ts,size,intraday)
    except Exception as e:
        logger.error('Error on fetching %s, Stop program!', ticker )
        logger.error(e)
        # sys.exit(1)


def get_daily_adjusted(ticker,ts,size,today_only):
    '''
    query from av in dict format
    return formated df
    '''
    data, meta_data = ts.get_daily_adjusted(ticker,outputsize=size)
    df = pd.DataFrame.from_dict(data).T
    df = df.drop(["7. dividend amount","8. split coefficient"], axis=1)
    df.columns = ["open","high","low","close","adjusted close","volume"]
    df = df[["open","high","low","close","adjusted close","volume"]]
    df.index = pd.to_datetime(df.index)
    if today_only:
        df = df.loc[df.index.max()].to_frame().T
        return df
    else:
        return df


def get_intraday(ticker,ts,size,intraday):
    '''
    query from av in dict format
    return formated df
    '''
    data, meta_data = ts.get_intraday(ticker,interval=intraday,outputsize=size)
    df = pd.DataFrame.from_dict(data).T
    df.columns = ["open","high","low","close","volume"]
    df = df[["open","high","low","close","volume"]]
    df.index.name = 'date'
    df.index = pd.to_datetime(df.index)
    if (size == 'compact'):
        # print(dt.today().strftime("%Y-%m-%d"))
        try:
            df = df.loc[dt.today().strftime("%Y-%m-%d")]
            return df
        except Exception as e:
            logger.debug(e)
            pass
    else:
        return df
