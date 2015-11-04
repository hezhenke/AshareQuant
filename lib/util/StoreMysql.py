# -*- coding:utf-8 -*-
"""
Created on 2015/09/28
@author: Jacob He
@contact: hezhenke123@163.com
"""
from sqlalchemy import create_engine
from lib import cons
import tushare as ts
import datetime
import sqlalchemy


def to_sql_attach_column(df,formName,dtype,cols={}):
    for k,v in cols.items():
        df.insert(len(df.columns),k,v)
    engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(cons.MYSQLDB_USER,
                                                         cons.MYSQLDB_PASS,
                                                         cons.MYSQLDB_HOST,
                                                         cons.MYSQLDB_DATABASE,
                                                         cons.MYSQLDB_CHARSET))
    df.to_sql(formName,engine,if_exists='append',dtype=dtype,index=False)
def store_all_data_to_mysql(method,formName):
    cur = datetime.datetime.now()
    curyear = cur.year
        
    retry_time = 4
    if method == 'get_report_data':
        dtype = {"distrib":sqlalchemy.types.VARCHAR(50)}
    for year in range(1989,curyear+1):
        for quarter in range(1,5):
            if ts.__dict__.has_key(method):
                df = ts.__dict__[method](year,quarter)
            if df is None:
                for _ in range(0,retry_time):
                    df = ts.__dict__[method](year,quarter)
                    if df is not None:
                        break
            if df is not None and not df.empty:
                to_sql_attach_column(df,formName,dtype,{'year':year,"quarter":quarter})
    
           