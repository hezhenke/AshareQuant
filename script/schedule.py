# -*- coding:utf-8 -*- 
"""
每日运行的脚本
Created on 2015/11/04
@author: Jacob He
@contact: hezhenke123@163.com
"""
import pandas as pd
from lib.stock.DbCache import DbCache
import lib.stock.trading as td
import lib.stock.fundamental as fd
import lib.cons as ct
from pymongo import MongoClient
from lib.util import dateu as du
import json
import numpy as np
from datetime import datetime
from datetime import timedelta

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def _parase_fq_factor(code):
    symbol = _code_to_symbol(code)
    try:
        request = Request(ct.HIST_FQ_FACTOR_URL%(symbol))
        request.add_header("User-Agent", ct.USER_AGENT)
        text = urlopen(request, timeout=20).read()
        text = text[1:len(text)-1]
        text = text.decode('utf-8') if ct.PY3 else text
        text = text.replace('{_', '{"')
        text = text.replace('total', '"total"')
        text = text.replace('data', '"data"')
        text = text.replace(':"', '":"')
        text = text.replace('",_', '","')
        text = text.replace('_', '-')
        text = json.loads(text)
        df = pd.DataFrame({'date':list(text['data'].keys()), 'fqprice':list(text['data'].values())})
        df['date'] = df['date'].map(_fun_except) # for null case
        if df['date'].dtypes == np.object:
            df['date'] = df['date'].astype(np.str)
        df = df.drop_duplicates('date')
        df = df.set_index("date")
        df = df.sort_index(ascending=False)
        df['fqprice'] = df['fqprice'].astype(float)
        return df
    except Exception as e:
        print(e)

def _code_to_symbol(code):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
    else:
        if len(code) != 6 :
            return ''
        else:
            return 'sh%s'%code if code[:1] in ['5', '6'] else 'sz%s'%code
        
def _fun_except(x):
    if len(x) > 10:
        return x[-10:]
    else:
        return x


if __name__ == '__main__':
    
    #更新基本面数据 
    
    cur = datetime.now()
    curyear = cur.year
    c = DbCache()
    c.check_db_cache(curyear)
    
    #更新历史数据
    date_fmt = '%Y-%m-%d'
    today = datetime.strftime(datetime.today(),date_fmt)
    '''获取股票代码列表'''
    stock_list = fd.get_stock_hq_list()
    '''逐个代码检查'''
    for code in stock_list['code']:
        '''获取复权价格'''
        fuquan_df = _parase_fq_factor(code)
        
        client = MongoClient(ct.MONGO_HOST, ct.MONGO_PORT)           
        cursor = client.stock["history_data"].find({"code":code}).sort([("date",-1)]).limit(1)
        if cursor.count() <= 0:
            print("%s is not in the db"%(code))
            '''重新采集数据灌进去'''
            
            if isinstance(fuquan_df, pd.DataFrame) and not fuquan_df.empty:
                start_date = fuquan_df.index.min()
                end_date = today
                if start_date is None or start_date == end_date:
                    continue
                df = td.get_h_data(code,start_date,end_date)                  
        else:
            tomorrow = datetime.strptime(cursor[0]['date'],date_fmt)+timedelta(days=1)
            start_date = datetime.strftime(tomorrow,date_fmt)
            end_date = today
            df = td.get_hist_data(code,start_date,end_date)
            df = df.reindex(columns=['open', 'high', 'close', 'low', 'volume'])
            df.insert(len(df.columns), "factor",0)
            df.insert(len(df.columns), "amount",0)
            df['volume'] = df['volume'] * 100
            for date in df.index:
                if date in fuquan_df.index:
                    df.loc[date,'factor'] = round(fuquan_df.loc[date,'fqprice']/df.loc[date,'close'],4)
            
            
        if isinstance(df, pd.DataFrame) and not df.empty:
            df.insert(len(df.columns), "code",code)
            df = df.reset_index()
            print("insert data to db of code:%s"%(code))
            client.stock["history_data"].insert(json.loads(df.to_json(orient='records')))
    
    
    