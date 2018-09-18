import pandas as pd
import sys
import logging
logger = logging.getLogger('main.alphaVantage')
from alpha_vantage.timeseries import TimeSeries

def get_av_daily_adjusted(ticker,size='compact',today_only=False):
    """
    size= compact or full, return df
    """
    try:
        ts = TimeSeries(key='6E970DLNQ4GZJDRF',output_format='pandas',indexing_type='date')
        return get_daily_adjusted(ticker,ts,size,today_only)
    except Exception as e:
        logger.error('Error on fetching %s, Stop program!', ticker )
        logger.error(e)
        sys.exit(1)


def get_daily_adjusted(ticker,ts,size,today_only):
    df, meta_data = ts.get_daily_adjusted(ticker,outputsize=size)
    df.columns = ["open","high","low","close","adjusted close","volume","dividend amount","split coefficient"]
    df = df[["open","high","low","close","adjusted close","volume"]]
    # print(df.head())
    df.index.name = 'date'
    df.index = pd.to_datetime(df.index)
    if today_only:
        df = df.loc[df.index.max()].to_frame().T
        return df
    else:
        return df
