# -*- coding: utf-8 -*-

''' 
    1 下载股票列表
    2 遍历股票列表下载网上的历史数据
    3 针对每一个代码，取出网上历史数据和mongo历史数据做对比
    4 如果mongo里面没有任何数据 则把所有数据插入mongo
    5 如果收盘价对不上，更新网上的数据到mongo
    
    6 每次计算重新算一遍 前复权价
    7 每次重新确定一遍是否重复
'''


from pymongo import MongoClient
import pandas as pd
import numpy as np
import lib.stock.trading as td
import lib.stock.fundamental as fd
import lib.cons as ct
from lib.util import dateu as du
import json
from datetime import datetime
from datetime import timedelta

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def get_adj_rate(code,stock_list,fuquan_df):
    frow = fuquan_df.head(1)
    rt = stock_list[stock_list.code == code]
    if rt.empty:
        return None
    if ((float(rt['high']) == 0) & (float(rt['low']) == 0)):
        preClose = float(rt['settlement'])
    else:
        if du.is_holiday(du.today()):
            preClose = float(rt['trade'])
        else:
            if (du.get_hour() > 9) & (du.get_hour() < 18):
                preClose = float(rt['settlement'])
            else:
                preClose = float(rt['trade'])
    
    rate = float(frow['fqprice']) / preClose
    return rate

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
        df = df.sort('date', ascending=False)
        df = df.set_index("date")
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

def run():
    
    #更新历史数据
    date_fmt = '%Y-%m-%d'
    today = datetime.strftime(datetime.today(),date_fmt)
    '''获取股票代码列表'''
    stock_list = td.get_stock_hq_list()

    '''逐个代码检查'''
    for code in stock_list['code']:
        '''获取复权价格'''
        fuquan_df = _parase_fq_factor(code)
        rate = get_adj_rate(code,stock_list,fuquan_df)
        
        client = MongoClient(ct.MONGO_HOST, ct.MONGO_PORT)           
        cursor = client[ct.MONGO_DATABASE]["history_data"].find({"code":code}).sort([("date",-1)]).limit(1)
        if cursor.count() <= 0:
            print("%s is not in the db"%(code))
            '''重新采集数据灌进去'''
            
            if isinstance(fuquan_df, pd.DataFrame) and not fuquan_df.empty:
                start_date = fuquan_df.index.min()
                end_date = today
                if start_date is None or start_date == end_date:
                    continue
                df = td.get_hist_data(code,start_date,end_date)  
        else:
            tomorrow = datetime.strptime(cursor[0]['date'],date_fmt)+timedelta(days=1)
            start_date = datetime.strftime(tomorrow,date_fmt)
            end_date = today
            df = td.get_hist_data(code,start_date,end_date)
            
            
        if isinstance(df, pd.DataFrame) and not df.empty:
            
            df = df.reindex(columns=['open', 'high', 'close', 'low', 'volume'])
            df.insert(len(df.columns), "factor",0)
            df.insert(len(df.columns), "adjclose",0)
            df['volume'] = df['volume'] * 100
            for date in df.index:
                if date in fuquan_df.index:
                    df.loc[date,'factor'] = round(fuquan_df.loc[date,'fqprice']/df.loc[date,'close'],4)
                    df.loc[date,'adjclose'] = round(fuquan_df.loc[date,'fqprice']/rate,2)
                    
            df.insert(len(df.columns), "code",code)
            df = df.reset_index()
            
            print("insert data to db of code:%s\n"%(code))
            #print json.loads(df.to_json(orient='records'))
            client[ct.MONGO_DATABASE]["history_data"].insert(json.loads(df.to_json(orient='records')))
        
        '''=================================================================================='''
        #核查数据
        cursor = client[ct.MONGO_DATABASE]["history_data"].find({"code":code}).sort([("date",-1)])
        hist_df = td.get_hist_data(code)
        duplicate_date_list = []
        
        if not isinstance(fuquan_df, pd.DataFrame) or not isinstance(hist_df, pd.DataFrame):
            continue
        
        for row in cursor:
            
            date = row['date']
            '''开始检查重复'''
            if date in duplicate_date_list:
                print("remove data to db of code:%s,%s\n"%(code,date))
                client[ct.MONGO_DATABASE]["history_data"].remove({"_id":row["_id"]})
                continue
            else:
                duplicate_date_list.append(row['date'])
                
                ''' 开始核对价格数据并更新前复权数据'''
            
            if date in hist_df.index and date in  fuquan_df.index:   
                close_diff = abs(row['close'] - hist_df.loc[date,'close'])
                adjclosediff = abs(row['adjclose'] - fuquan_df.loc[date,'fqprice']/rate)
                
                #允许误差0.2
                if close_diff > 0.2 or adjclosediff > 0.2:
                    update_item = {}
                    update_item['open'] = round(hist_df.loc[date,'open'],2)
                    update_item['high'] = round(hist_df.loc[date,'high'],2)
                    update_item['low'] = round(hist_df.loc[date,'low'],2)
                    update_item['close'] = round(hist_df.loc[date,'close'],2)
                    update_item['adjclose'] = round(fuquan_df.loc[date,'fqprice']/rate,2)
                    update_item['factor'] = round(fuquan_df.loc[date,'fqprice']/update_item['close'],4)
                    update_item['volume'] = hist_df.loc[date,'volume'] * 100
                    print("update data to db of code:%s,%s\n"%(code,date))
                    #print update_item
                    client[ct.MONGO_DATABASE]["history_data"].update({"_id":row["_id"]},{"$set":update_item})
                    
            elif date in  fuquan_df.index:
                adjclosediff = abs(row['adjclose'] - fuquan_df.loc[date,'fqprice']/rate)
                #允许误差0.2
                if adjclosediff > 0.2:
                    update_item = {}
                    update_item['adjclose'] = round(fuquan_df.loc[date,'fqprice']/rate,2)
                    update_item['factor'] = round(fuquan_df.loc[date,'fqprice']/row['close'],4)
                    print("update data to db of code:%s,%s\n"%(code,date))
                    #print update_item
                    client[ct.MONGO_DATABASE]["history_data"].update({"_id":row["_id"]},{"$set":update_item})
if __name__ == '__main__':
    
    run()