import logging
import sys
import yaml,os
import pandas as pd
from db.remove import *
from db.write import *
from db.read import read_table_df_Engine,read_table_df_nodrop_Engine
logger = logging.getLogger('main.rbreaker')


def rbreaker(engine_simulation, engine_dailydb):
    try:
        with open("config.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except Exception as e:
        logger.error('No DB connection info or config file not found!')
        logger.error(e)
        sys.exit(1)

    # reads subscribe -  config.yaml
    subscribes = cfg['Rbreaker']['sub']
    # if there are subscribers
    if subscribes:
        # ticker is in xx.to format
        for ticker in subscribes:
            day = read_table_df_Engine(ticker,engine_dailydb).iloc()[-1]
            date = day.name
            high = day.high
            close = day.close
            low = day.low
            foreseen_sell = high + 0.35 * (close - low)
            foreseen_buy = low - 0.35 * (high - close)
            reverse_sell = 1.07 / 2 * (high + low) - 0.07 * low
            reverse_buy = 1.07 / 2 * (high + low) - 0.07 * high
            breakout_buy = foreseen_sell + 0.25 * (foreseen_sell - foreseen_buy)
            breakout_sell = foreseen_buy - 0.25 * (foreseen_sell - foreseen_buy)
            # R-Breaker dict
            dict_rbreaker = {'date':date, 'ticker':ticker, 'foreseen_sell':round(foreseen_sell,2),'foreseen_buy':round(foreseen_buy,2),'reverse_sell':round(reverse_sell,2),'reverse_buy':round(reverse_buy,2),'breakout_buy':round(breakout_buy,2),'breakout_sell':round(breakout_sell,2)}
            # R-Breaker dataframe
            df_rbreaker = pd.DataFrame.from_records([dict_rbreaker],index='date')
            df_rbreaker.index = pd.to_datetime(df_rbreaker.index)
            # delete rows that have specific ticker name in 'ticker' filed - remove.py
            delete_by_fieldValue_Engine('rbreaker','ticker',ticker,engine_simulation)
            # write df to sql - write.py
            df_to_sql_prikey('rbreaker',df_rbreaker,engine_simulation,'date')
            logger.debug('updating %s for %s' % (date,ticker))
