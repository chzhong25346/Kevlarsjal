import re
import sys
from .sortBy import sort_by_industry
this = sys.modules[__name__]

def get_indCode(data):
    '''
    return dic map {abbreviation of ind code : Insdustry name}
    '''
    ind_list = data['Industry'].unique().tolist()
    short_ind_list = []
    for i in ind_list:
        i = re.sub('[^A-Za-z0-9]+', ' ', i).split()
        if( len(i) == 1 ):
            i = i[0][:3]
        else:
            new_list = []
            for item in i:
                new_list.append(item[0])
            i = ''.join(new_list)
        short_ind_list.append(i.lower())
        
    return dict(zip(short_ind_list, ind_list))


def indCode_to_tickers(data):
    '''
    Return dic of {ind_cod:df}; Industry Code is a df that contains its tickers
    '''
    ind_dic = get_indCode(data)
    df_dic = {}
    for key, value in ind_dic.items():
        df = sort_by_industry(data,value).set_index('Symbol')
        df_dic.update({key: df})

    return df_dic
