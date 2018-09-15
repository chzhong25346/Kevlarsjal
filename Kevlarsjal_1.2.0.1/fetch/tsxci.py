import urllib3,certifi
import pandas as pd
import numpy as np

def get_tsxci_table():
    '''
    Query Wiki page and return table in df format
    '''
    https = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(),)
    page= 'https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index'
    url = https.urlopen('GET',page)
    data = pd.read_html(url.data,header=0)
    data[0].columns = ['Symbol', 'Company', 'Sector', 'Industry']

    return data[0]
