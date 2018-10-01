import logging
import pandas as pd
import numpy as np

logger = logging.getLogger('main.normalize')


def normalize_tsxci(data):
    '''
    replace . to -
    replace "VRX" to "BHC" and its company name accordingly
    '''
    data['Symbol'] = data['Symbol'].str.replace(".","-")
    #Bausch Health Companies Inc. (formerly Valeant Pharmaceuticals) to new ticker code VRX -> BHC
    data['Symbol'] = data['Symbol'].str.replace("VRX","BHC")
    data['Company'] = data['Company'].str.replace("Valeant Pharmaceuticals International Inc.","Bausch Health Companies Inc.")
    return data


def type_to_int(df,removeItem):
    '''
    convert columns to dtype int except specified value in column list
    '''
    saved_series = df[removeItem]
    columnL=df.columns.tolist()
    # if a big list includes a list
    if set(removeItem).issubset(columnL):
        columnL = [x for x in columnL if (x not in removeItem)]
    df[columnL].apply(lambda x: x.astype('int'))
    df[removeItem] = saved_series
    return df


def groupby_na_to_zero(df, index_name):
    '''
    groupby indexname using first()
    fill NA with 0
    '''
    df = df.groupby(index_name).first()
    df.fillna(0, inplace=True)
    return df
