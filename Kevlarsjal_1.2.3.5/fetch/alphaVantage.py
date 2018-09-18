import pandas as pd
import sys
import logging
import json
from alpha_vantage.timeseries import TimeSeries
logger = logging.getLogger('main.alphaVantage')

def get_av_daily_adjusted(ticker,size='compact',today_only=False):
    """
    size= compact or full, return df
    """
    try:
        ts = TimeSeries(key='6E970DLNQ4GZJDRF',indexing_type='date')
        return get_daily_adjusted(ticker,ts,size,today_only)
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
    df.columns = ["open","high","low","close","adjusted close","volume","dividend amount","split coefficient"]
    df = df[["open","high","low","close","adjusted close","volume"]]
    df.index = pd.to_datetime(df.index)
    if today_only:
        df = df.loc[df.index.max()].to_frame().T
        return df
    else:
        return df
