import sys
import logging
import yaml,os
logger = logging.getLogger('main.mysql')
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

def create_dbengine(db='tsxci_daily_db'):
    '''
    return engine/connection
    '''
    try:
        with open("config.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except Exception as e:
        logger.error('No DB connection info or config file not found!')
        logger.error(e)
        sys.exit(1)

    db_username = cfg['mysql']['username']
    db_password = cfg['mysql']['password']
    db_ip = cfg['mysql']['ip']
    db_port = cfg['mysql']['port']
    tsxci_daily_db = cfg['mysql']['tsxci_daily_db']
    tsxci_intraday_db = cfg['mysql']['tsxci_intraday_db']

    if (db=='tsxci_daily_db'):
        url = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username,db_password,db_ip,db_port,tsxci_daily_db)
        logger.debug('connecting to %s', url)
    if (db=='tsxci_intraday_db'):
        url = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username,db_password,db_ip,db_port,tsxci_intraday_db)
        logger.debug('connecting to %s', url)

    return create_engine(url)
