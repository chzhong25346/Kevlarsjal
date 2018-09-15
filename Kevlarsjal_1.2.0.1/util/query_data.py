import time
import sys
from fetch.alphaVantage import get_av_daily_adjusted


def get_df_bySec(sec_code,size='full',today_only=False,sleep_timer=15):
    '''
    return {"ticker.TO":df}
    '''
    ticker_list = sec_code.index.tolist()
    dic = {}
    for ticker in ticker_list:
        ticker = (ticker+'.TO').lower()
        time.sleep(sleep_timer)
        df = get_av_daily_adjusted(ticker,size,today_only)
        dic.update({ticker:df})

    return dic
