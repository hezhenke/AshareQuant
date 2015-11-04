# -*- coding:utf-8 -*-
"""
Created on 2015/09/28
@author: Jacob He
@contact: hezhenke123@163.com
"""
import lib.stock.WrapperFundamental.WrapperFundamental as fd


from sqlalchemy import create_engine
from lib import cons
import datetime
import sqlalchemy


def store(df,tableName,dtype,attach_cols={}):
    for k,v in attach_cols.items():
        df.insert(len(df.columns),k,v)
    engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(cons.MYSQLDB_USER,
                                                         cons.MYSQLDB_PASS,
                                                         cons.MYSQLDB_HOST,
                                                         cons.MYSQLDB_DATABASE,
                                                         cons.MYSQLDB_CHARSET))
    df.to_sql(tableName,engine,if_exists='append',dtype=dtype,index=False)
    
    
def store_all(method,tableName):
    cur = datetime.datetime.now()
    curyear = cur.year
        
    retry_time = 4
    dtype = None
    if method == 'get_report_data':
        dtype = {"distrib":sqlalchemy.types.VARCHAR(50)}
    for year in range(2010,curyear+1):
        for quarter in range(1,5):
            if fd.__dict__.has_key(method):
                df = fd.__dict__[method](year,quarter)
            if df is None:
                for _ in range(0,retry_time):
                    df = fd.__dict__[method](year,quarter)
                    if df is not None:
                        break
            if df is not None and not df.empty:
                store(df,tableName,dtype,{'year':year,"quarter":quarter})
                
if __name__ == '__main__':
    
    store_all("get_growth_data","growth_data")
    #获取业绩报表
    #store_all("get_report_data","report_data")
    '''
    #获取盈利数据
    store_all("get_profit_data","profit_data")
    
    #获取营运能力数据
    store_all("get_operation_data","operation_data")
    
    
    #获取成长能力数据
    store_all("get_growth_data","growth_data")
    
    #获取偿债能力数据
    store_all("get_debtpaying_data","debtpaying_data")
    
    #获取偿债能力数据
    store_all("get_cashflow_data","cashflow_data")
    '''