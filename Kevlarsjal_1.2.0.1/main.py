import sys
from db.mysql import create_dbengine
from db.write import df_to_sql
from fetch.tsxci import get_tsxci_table
from util.indCode import get_indCode,indCode_to_tickers
from util.query_data import get_df_bySec

def main():

    data = get_tsxci_table()

    ic_dic = indCode_to_tickers(data)
    bs = ic_dic['bs']

    df_dic = get_df_bySec(bs,size='full',today_only=False,sleep_timer=15)
    df_to_sql(df_dic)


if __name__ == '__main__':
    sys.exit(main())
