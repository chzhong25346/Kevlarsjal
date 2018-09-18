import time
import sys
import logging
logger = logging.getLogger('main.query_data')
from fetch.alphaVantage import get_av_daily_adjusted
from db.write import df_to_sql
from db.mysql import create_dbengine


def get_df_bySec(sec_code,size,today_only,sleep_timer):
    '''
    extract ticker_list from sec_code. symbols of that sector; query and write
    '''
    ticker_list = sec_code.index.tolist()
    query_and_write(ticker_list,size,today_only,sleep_timer)


def get_df_byTicker(data,size,today_only,sleep_timer):
    '''
    extract ticker_list from data. That's all symbols; query and write
    '''
    ticker_list = data['Symbol'].tolist()
    query_and_write(ticker_list,size,today_only,sleep_timer)


def query_and_write(ticker_list,size='full',today_only=False,sleep_timer=15):
    '''
    Looping through ticker list, query df and write it to DB immediately
    '''
    engine = create_dbengine()
    try:
        # Looping through the ticker list
        for ticker in ticker_list:
            ticker = (ticker+'.TO').lower()
            time.sleep(sleep_timer)
            logger.debug('Fetching %s', ticker)
            df = get_av_daily_adjusted(ticker,size,today_only)
            # writing df to db
            df_to_sql({ticker:df},engine)

    except Exception:
        logger.error('Querying data failed!')
