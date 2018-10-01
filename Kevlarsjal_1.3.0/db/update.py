import sys
import pandas as pd
import logging
logger = logging.getLogger('main.update')
from .mysql import create_dbengine


def update_Engine(tname,sentence,field,value,engine):
    '''
    sentence is what's to updated
    require a engine
    '''
    try:
        engine.execute('UPDATE `{0}` SET {1} WHERE `{2}` = "{3}";'.format(tname,sentence,field,value))
    except Exception as e:
        logger.debug(e)
        return False
