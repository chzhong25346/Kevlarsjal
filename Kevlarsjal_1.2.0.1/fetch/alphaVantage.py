import pandas as pd
from alpha_vantage.timeseries import TimeSeries

def get_av_daily_adjusted(ticker,size='compact',today_only=False):
    """
    size= compact or full
    """
    ts = TimeSeries(key='6X6P224DS04C2GRO',output_format='pandas',indexing_type='date')
    df, meta_data = ts.get_daily_adjusted(ticker,outputsize=size)
    df.columns = ["open","high","low","close","adjusted close","volume","dividend amount","split coefficient"]
    df = df[["open","high","low","close","adjusted close","volume"]]
    df.index.name = 'date'
    df.index = pd.to_datetime(df.index)
    if today_only:
        df = df.loc[df.index.max()].to_frame().T
        return df
    else:
        return df
