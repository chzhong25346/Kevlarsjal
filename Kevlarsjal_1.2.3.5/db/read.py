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


def read_table_df_Engine(tname,engine):
    '''
    Read teable return df; index='date'; an enginre is required
    '''
    try:
        df = pd.read_sql_table(tname,engine,index_col='date')
        # all columns are object except for Index
        cols = df.columns[df.dtypes.eq(object)]
        for c in cols:
            # change dtype to numeric
            df[c] = pd.to_numeric(df[c], errors='coerce')
            # drop any row with 0
            df = df[(df.T != 0).any()]
        return df
    except Exception as e:
        logger.debug('Cannot read table! - continue')
        return False
