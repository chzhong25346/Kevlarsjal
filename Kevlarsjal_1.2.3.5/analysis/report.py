import logging
import pandas as pd
import datetime as dt
from db.read import read_table_df_Engine
from db.mysql import create_dbengine
from db.write import report_df_to_sql
from fetch.StockIndex import get_index_table
from util.normalize import type_to_int,groupby_na_to_zero
from log.mail import sendMail
from .ema import trend_potential
from .volume import unusual_volume
from .fiftytwoWeek import fiftytwo_week
from .pattern import find_pattern
logger = logging.getLogger('main.report')


def report(index_name):
    '''
    '''
    # index table in df
    indexT = get_index_table(index_name)
    # index df to list of symbols
    tickerL = indexT['Symbol'].tolist()
    # daily db engine
    engine_dailydb = create_dbengine(db=index_name+"_daily_db")
    # report db engine
    engine_report = create_dbengine(db=index_name+"_report")
    # temp df for report
    report_df = pd.DataFrame()
    for ticker in tickerL:
        # equity name
        equity = ticker
        # ticker + '.to'
        ticker_to = (ticker+'.to').lower()
        # read daily db return df
        df = read_table_df_Engine(ticker_to,engine_dailydb)
        # unusual volume stickers append to df
        report_df = report_df.append(unusual_volume(equity,df),ignore_index=True)
        # unusual trend stickers append to df
        report_df = report_df.append(trend_potential(equity,df),ignore_index=True)
        # 52w high/low/trending append to df
        report_df = report_df.append(fiftytwo_week(equity,df),ignore_index=True)
        # decide if known pattern append to df
        report_df = report_df.append(find_pattern(equity,df),ignore_index=True)
    # ticker columns as index
    # report_df.set_index('ticker', inplace=True)
    # grouby using first() and NaN to Zero
    report_df = groupby_na_to_zero(report_df, 'ticker')
    report_df = type_to_int(report_df,'pattern')
    # tname is today's date
    tname = dt.datetime.today().strftime("%m-%d-%Y")
    # write df into db
    report_df_to_sql(tname,report_df,engine_report)
    email(tname)



def email(tname):
    sub = 'Report ready for %s' % (tname)
    cont = 'table is %s' % (tname)
    sendMail(sub,cont)
