
from sqlalchemy import create_engine

def data_to_db(data, tablename):
    engine_k = create_engine("mssql+pymssql://sa:Head609900@10.128.4.201:2022/yntp", echo=True)
    # ! 入库操作前做好数据备份, 
    # if_exits 参数慎重选择，否则会删除原有库表
    # * replace: Drop the table before inserting new values
    # * append: Insert new values to the existing table
    data.to_sql(name=tablename, con=engine_k, if_exists='replace', index=None)