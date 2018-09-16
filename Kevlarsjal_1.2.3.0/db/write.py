import sys
import pandas as pd
import logging
logger = logging.getLogger('main.write')
from .mysql import create_dbengine

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
                    pass
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
