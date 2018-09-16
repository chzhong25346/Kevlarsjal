import sys
from db.mysql import create_dbengine
from db.write import df_to_sql
from fetch.StockIndex import get_index_table
from util.indCode import get_indCode,indCode_to_tickers
from util.query_data import get_df_bySec,get_df_byTicker

def update_all(index_name,type='compact'):
    '''
    update all
    full: all data
    compact: today only
    '''
    data = get_index_table(index_name)
    if (type=='compact'):
        df_dic = get_df_byTicker(data,size='compact',today_only=True,sleep_timer=15)
    else:
        df_dic = get_df_byTicker(data,size='full',today_only=False,sleep_timer=15)


def update_by_industry(index_name,indCode,type='full'):
    '''
    update by industry code;
    full: all data
    compact: today only
    '''
    data = get_index_table(index_name)
    df = indCode_to_tickers(data,indCode)
    if (type=='compact'):
        df_dic = get_df_bySec(df,size='compact',today_only=True,sleep_timer=15)
    else:
        df_dic = get_df_bySec(df,size='full',today_only=False,sleep_timer=15)


# def update_index(index_name):
#     data = get_index_table(index_name)
#     df_dic = {index_name:data}
#     df_to_sql(df_dic)
