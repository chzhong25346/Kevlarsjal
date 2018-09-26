import sys
import pandas as pd
import logging
logger = logging.getLogger('main.write')
from .mysql import create_dbengine
from sqlalchemy.types import VARCHAR

def df_to_sql(dic,engine):
    '''
    Date is primary key and not null
    Create table if not exists and insert rows from df.
    Append rows if not duplicated
    '''
    # engine = create_dbengine()
    try:
        for key, value in dic.items():
            if engine.dialect.has_table(engine,key):
                try:
                    value.to_sql(key, engine, index=True,index_label='date',if_exists='append')
                    logger.debug('writing table %s', key)
                except Exception as e:
                    logger.error(e)
            else:
                if(key != 'tsxci'):
                    value.to_sql(key, engine, index=True,index_label='date',if_exists='append')
                    engine.execute('ALTER TABLE `{0}`MODIFY COLUMN `date` datetime NOT NULL FIRST,ADD PRIMARY KEY (`date`);'.format(key))
                    logger.debug('writing table %s', key)
                else:
                    value.to_sql(key, engine, index=True,index_label='date',if_exists='append')
                    logger.debug('writing table %s', key)

    except Exception as e:
        logger.error(e)


def report_df_to_sql(tname,df,engine):
    '''
    saving report
    'ticker' as primary key is hardcoded
    '''
    try:
        if engine.dialect.has_table(engine,tname):
            try:
                df.to_sql(tname, engine, index=True,index_label='ticker',if_exists='append',
                        dtype={'ticker': VARCHAR(df.index.get_level_values('ticker').str.len().max())})
                logger.debug('writing table %s', tname)
            except Exception as e:
                logger.error(e)
        else:
            df.to_sql(tname, engine, index=True,index_label='ticker',if_exists='append',
                    dtype={'ticker': VARCHAR(df.index.get_level_values('ticker').str.len().max())})
            engine.execute('ALTER TABLE `{0}` MODIFY COLUMN `ticker`  varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL FIRST ,ADD PRIMARY KEY (`ticker`);'.format(tname))
            logger.debug('writing table %s', tname)
    except Exception as e:
        logger.error(e)
