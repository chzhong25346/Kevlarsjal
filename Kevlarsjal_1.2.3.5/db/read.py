import sys
import pandas as pd
import logging
logger = logging.getLogger('main.read')
from .mysql import create_dbengine


def read_table_df(tname):
    '''
    Read teable return df; index='date'
    '''
    engine = create_dbengine()
    try:
        df = pd.read_sql_table(tname,engine,index_col='date')
        return df
    except:
        logger.debug('Cannot read table! - continue')
        return False
