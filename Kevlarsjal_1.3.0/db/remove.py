import sys
import pandas as pd
import logging
logger = logging.getLogger('main.remove')
from .mysql import create_dbengine


def delete_by_fieldValue_Engine(tname,field,value,engine):
    '''
    delete row(s) by field = 'value'
    require a engine
    '''
    try:
        engine.execute('DELETE FROM `{0}` WHERE `{1}` = "{2}";'.format(tname,field,value))
    except Exception as e:
        logger.debug('no [%s]table found! - continue', tname)
        return False
