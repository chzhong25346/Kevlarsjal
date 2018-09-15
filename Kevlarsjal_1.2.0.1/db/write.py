import pandas as pd
from .mysql import create_dbengine

username = "colin"
password = "123456a"
ip = "192.168.0.18"
name = "tsxci_daily"


def df_to_sql(dic):
    '''
    Date is primary key and not null
    Create table if not exists and insert rows from df.
    Append rows if not duplicated
    '''
    engine = create_dbengine(username,password,ip,name)

    for key, value in dic.items():
        if engine.dialect.has_table(engine,key):
            try:
                value.to_sql(key, engine, index=True,index_label='date',if_exists='append')
            except Exception as e:
                pass
        else:
            value.to_sql(key, engine, index=True,index_label='date',if_exists='append')
            engine.execute('ALTER TABLE `{0}`MODIFY COLUMN `date` datetime NOT NULL FIRST,ADD PRIMARY KEY (`date`);'.format(key))
