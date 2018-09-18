import re
import sys
import logging
from .sortBy import sort_by_industry
this = sys.modules[__name__]
logger = logging.getLogger('main.indCode')

def get_indCode(data):
    '''
    return dic map {abbreviation of ind code : Insdustry name}
    '''
    try:
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
        if short_ind_list:
            logger.debug('Generated %s Industry codes' % len(short_ind_list))
            return dict(zip(short_ind_list, ind_list))
    except Exception:
        logger.error('Error on generating Industry codes!')


def indCode_to_tickers(data,code):
    '''
    Return dic of {ind_cod:df}; Industry Code is a df that contains its tickers
    '''
    ind_dic = get_indCode(data)
    df_dic = {}
    for key, value in ind_dic.items():
        df = sort_by_industry(data,value).set_index('Symbol')
        df_dic.update({key: df})
    logger.debug('Found %s stocks in %s' % (len(df_dic[code]), code))

    return df_dic[code]
