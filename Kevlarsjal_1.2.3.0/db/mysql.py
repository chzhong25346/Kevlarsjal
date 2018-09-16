import sys
import logging
import yaml,os
logger = logging.getLogger('main.mysql')
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

def create_dbengine():
    '''
    return engine/connection
    '''
    try:
        with open("config.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except Exception:
        logger.error('No DB connection info or config file not found!')
        sys.exit(1)

    db_username = cfg['mysql']['username']
    db_password = cfg['mysql']['password']
    db_ip = cfg['mysql']['ip']
    db_name = cfg['mysql']['name']
    db_port = cfg['mysql']['port']

    url = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username,db_password,db_ip,db_port,db_name)
    logger.debug('connecting to %s', url)

    return create_engine(url)
