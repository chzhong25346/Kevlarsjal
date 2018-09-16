import logging
import urllib3,certifi
import pandas as pd
import numpy as np
from db.read import read_table_df
from db.write import df_to_sql
from db.mysql import create_dbengine

logger = logging.getLogger('main.StockIndex')

def get_index_table(tname):
    '''
    Read table if exists,return df
    otherwise, query Wiki page for tsxci and
    write table
    and return table in df format
    '''
    engine = create_dbengine()
    # if table exists in db
    if read_table_df(tname) is not False:
        # return df
        return read_table_df(tname)
    elif (tname == 'tsxci'):
        https = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(),)
        page= 'https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index'
        try:
            url = https.urlopen('GET',page)
            page_d = pd.read_html(url.data,header=0,keep_default_na=False) # NA -> NaN is National Bank of Canada 
            page_d[0].columns = ['Symbol', 'Company', 'Sector', 'Industry']
            data = page_d[0]
            data['Symbol'] = data['Symbol'].str.replace(".","-")
            logger.debug('Connected Wiki, total: %s symbols listed' % (len(data)-1))
            df_to_sql({tname:data},engine) # writing only if index table not exists
            return data
        except Exception:
            logger.error('Failed to establish a new connection to WiKi')
