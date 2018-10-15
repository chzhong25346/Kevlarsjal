import time
import sys
import logging
logger = logging.getLogger('main.query_data')
from fetch.alphaVantage import get_av
from db.write import df_to_sql
from db.mysql import create_dbengine


def get_df_bySec(sec_code,intraday,size,today_only,sleep_timer):
    '''
    extract ticker_list from sec_code. symbols of that sector; query and write
    '''
    ticker_list = sec_code.index.tolist()
    query_and_write(ticker_list,intraday,size,today_only,sleep_timer)


def get_df_byTicker(data,intraday,size,today_only,sleep_timer):
    '''
    extract ticker_list from data. That's all symbols; query and write
    '''
    ticker_list = data['Symbol'].tolist()
    # ticker_list = ['YRI']
    query_and_write(ticker_list,intraday,size,today_only,sleep_timer)


def query_and_write(ticker_list,intraday,size='full',today_only=False,sleep_timer=15):
    '''
    Looping through ticker list, query df and write it to DB immediately
    '''
    if (intraday == 'none'): # daily
        engine = create_dbengine(db='tsxci_daily_db')
    elif (intraday != 'none'): # intraday
        engine = create_dbengine(db='tsxci_intraday_db')

    try:
        # Looping through the ticker list
        for ticker in ticker_list:
            ticker = (ticker+'.TO').lower()
            time.sleep(sleep_timer)
            logger.debug('Fetching %s', ticker)
            # querying df from av
            df = get_av(ticker,size,today_only,intraday)
            if (intraday == 'none'): # daily
                # writing df to db
                df_to_sql({ticker:df},engine)
            elif (intraday != 'none'): # intraday
                # writing df to db
                df_to_sql({ticker:df},engine)

    except Exception:
        logger.error('Querying data failed!')



############ New Function #####################

def fetch_write(index_name,data,intraday,size='full',today_only=False,sleep_timer=15):
    '''
    Looping through ticker list, query df and write it to DB immediately
    '''
    ticker_list = data['Symbol'].tolist()
    # ticker_list = ['XUT']
    if (index_name == 'tsxci'):
        if (intraday == 'none'): # daily
            engine = create_dbengine(db='tsxci_daily_db')
        elif (intraday != 'none'): # intraday
            engine = create_dbengine(db='tsxci_intraday_db')
    # ca_etf will be in tsxci daily database because it's hard to change simulator
    elif (index_name == 'ca_etf'):
            engine = create_dbengine(db='tsxci_daily_db')
    try:
        # Looping through the ticker list
        for ticker in ticker_list:
            ticker = (ticker+'.TO').lower()
            time.sleep(sleep_timer)
            logger.debug('Fetching %s', ticker)
            # querying df from av
            df = get_av(ticker,size,today_only,intraday)
            if (intraday == 'none'): # daily
                # writing df to db
                df_to_sql({ticker:df},engine)
            elif (intraday != 'none'): # intraday
                # writing df to db
                df_to_sql({ticker:df},engine)

    except Exception:
        logger.error('Querying data failed!')
