import os,sys
from db.mysql import create_dbengine
from db.write import df_to_sql
from fetch.StockIndex import get_index_table
from util.indCode import get_indCode, indCode_to_tickers
from util.query_data import get_df_bySec, get_df_byTicker, fetch_write
from analysis.report import report
from simulation.simulator import simulator

sys.path.insert(0, os.path.abspath(".."))

def update_all(index_name,intraday,type='compact'):
    '''
    update all
    full: all data
    compact: today only
    '''
    data = get_index_table(index_name) # All tickers in DF format
    # Use old function 'get_df_byTicker' ) NO index_name
    if (index_name == 'tsxci'):
        if (type=='compact' and intraday=='none'):
            df_dic = get_df_byTicker(data,intraday='none',size='compact',today_only=True,sleep_timer=15)
        elif (type=='full' and intraday=='none'):
            df_dic = get_df_byTicker(data,intraday='none',size='full',today_only=False,sleep_timer=15)
        elif (type=='compact' and intraday !='none'):
            df_dic = get_df_byTicker(data,intraday,size='compact',today_only=True,sleep_timer=15)
        elif (type=='full' and intraday !='none'):
            df_dic = get_df_byTicker(data,intraday,size='full',today_only=False,sleep_timer=15)
        else:
            pass
    # New function is called "fetch_write" for ca_etf
    elif (index_name == 'ca_etf'):
        if (type=='compact' and intraday=='none'):
            df_dic = fetch_write(index_name,data,intraday='none',size='compact',today_only=True,sleep_timer=15)
        elif (type=='full' and intraday=='none'):
            df_dic = fetch_write(index_name,data,intraday='none',size='full',today_only=False,sleep_timer=15)
        else:
            pass


def update_by_industry(index_name,indCode,intraday,type='full'):
    '''
    update by industry code;
    full: all data
    compact: today only
    '''
    data = get_index_table(index_name)
    df = indCode_to_tickers(data,indCode)  # ticers in that Industry in DF format
    if (type=='compact' and intraday=='none'):
        df_dic = get_df_bySec(df,intraday='none',size='compact',today_only=True,sleep_timer=15)
    elif (type=='full' and intraday=='none'):
        df_dic = get_df_bySec(df,intraday='none',size='full',today_only=False,sleep_timer=15)
    elif (type=='compact' and intraday!='none'):
        df_dic = get_df_bySec(df,intraday,size='compact',today_only=True,sleep_timer=15)
    elif (type=='full' and intraday!='none'):
        df_dic = get_df_bySec(df,intraday,size='full',today_only=False,sleep_timer=15)
    else:
        pass


def reporting(index_name,indCode,intraday,type):
    '''
    run report in analysis folder
    '''
    report(index_name)


def simulating(index_name,indCode,intraday,type):
    '''
    run simulation in analysis folder
    '''
    simulator(index_name)
