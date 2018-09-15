from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

def create_dbengine(db_username,db_password,db_ip,db_name,port=3306):
    '''
    return engine/connection
    '''
    return create_engine('mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username,db_password,db_ip,port,db_name))
