import logging
import urllib3,certifi
import pandas as pd
import numpy as np
from db.read import read_table_df_eng
from db.write import df_to_sql
from db.mysql import create_dbengine
from util.normalize import normalize_tsxci, normalize_ca_etf

logger = logging.getLogger('main.StockIndex')

def get_index_table(tname):
    '''
    Read table if exists,return df
    otherwise, query Wiki page for tsxci and
    write table
    and return table in df format
    '''
    # Query TSXCI index from WiKi
    if (tname == 'tsxci'):
        # engine by default for tsxci_daily_db
        engine = create_dbengine()
        # Table Already Exists, then Read Table
        if read_table_df_eng(tname,engine) is not False:
            # return df
            return read_table_df_eng(tname,engine)
        else:
            page= 'https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index'
            https = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(),)
            try:
                url = https.urlopen('GET',page)
                page_d = pd.read_html(url.data,header=0,keep_default_na=False) # NA -> NaN is National Bank of Canada
                page_d[0].columns = ['Symbol', 'Company', 'Sector', 'Industry']
                data = page_d[0]
                data = normalize_tsxci(data)
                logger.debug('Connected Wiki, total: %s symbols listed' % (len(data)-1))
                df_to_sql({tname:data},engine) # writing only if index table not exists
                return data
            except Exception as e:
                # logger.error('Failed to establish a new connection to WiKi')
                logger.error(e)
    # Query iTrade Commision free ETF table
    elif (tname == 'ca_etf'):
        # engine by default for tsxci_daily_db
        engine = create_dbengine()
        # Table Already Exists, then Read Table
        if read_table_df_eng(tname,engine) is not False:
            # return df
            return read_table_df_eng(tname,engine)
        else:
            page= 'https://www.scotiabank.com/itrade/en/0,,4200,00.html'
            https = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(),)
            try:
                url = https.urlopen('GET',page)
                page_d = pd.read_html(url.data,header=0,keep_default_na=False) # NA -> NaN is National Bank of Canada
                # Industry = Sector, easy for reporting
                page_d[0].columns = ['Symbol', 'Market', 'Description', 'Industry']
                data = page_d[0]
                data = normalize_ca_etf(data)
                logger.debug('Connected iTrade, total: %s symbols listed' % (len(data)-1))
                df_to_sql({tname:data},engine) # writing only if index table not exists
                return data
            except Exception as e:
                # logger.error('Failed to establish a new connection to WiKi')
                logger.error(e)
