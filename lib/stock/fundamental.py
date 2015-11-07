# -*- coding:utf-8 -*- 
"""
基本面数据接口 
Created on 2015/09/09
@author: Jacob He
@contact: hezhenke123@163.com
"""
import pandas as pd
from lib import cons as ct
from lib.stock import cache
import json
import os
from pandas.compat import StringIO
from urllib import quote
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
    
def get_stock_basics():
    """
        获取沪深上市公司基本情况
    Return
    --------
    DataFrame
               code,代码
               name,名称
               industry,细分行业
               area,地区
               pe,市盈率
               outstanding,流通股本
               totals,总股本(万)
               totalAssets,总资产(万)
               liquidAssets,流动资产
               fixedAssets,固定资产
               reserved,公积金
               reservedPerShare,每股公积金
               eps,每股收益
               bvps,每股净资
               pb,市净率
               timeToMarket,上市日期
    """
    stock_basics_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'data','all_stock.csv')
    text = None
    file_obj = open(stock_basics_file)
    try:
        text = file_obj.read()
        text = text.decode('GBK')
        text = text.replace('--', '')
    finally:
        file_obj.close()
    if text is not None:
        df = pd.read_csv(StringIO(text), dtype={'code':'object'})
        df = df.set_index('code')
        return df

def get_stock_hq_list():
    """
        获取沪深上市公司列表和行情
    Return
    --------
    DataFrame    
            guba,股吧地址
            symbol,股票代号
            code,股票代码
            name,股票名称
            trade,最新价
            pricechange,涨跌额
            changepercent,涨跌幅
            buy,买入
            sell,卖出
            settlement,昨收
            open,今开
            high,最高
            low,最低
            volume,成交量（手）
            amount,成交额（万）
            ticktime,
            per,市盈率
            per_d,动态市盈率
            nta,每股净资产
            pb,市净率
            mktcap,总市值
            nmc,流通市值
            turnoverratio,换手率(%)
            favor,
            guba,
               
    """
    ct._write_head()
    df =  _get_stock_hq_list(1, pd.DataFrame())
    if df is not None and not df.empty:
        df = df.drop_duplicates('code')
        df['code'] = df['code'].map(lambda x:str(x).zfill(6))
    return df
def _get_stock_hq_list(pageNo, dataArr):
    ct._write_console()
    try:
        #param:["hq","hs_a","{sort}",{asc},{page},{num}]
        hq_list_param = '["hq","hs_a","",0,%d,%d]'%(pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(hq_list_param,',[]')))
        request.add_header("User-Agent", ct.USER_AGENT)
        text = urlopen(request, timeout=ct.API_TIMEOUT).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'], columns=js[0]['fields'])
        dataArr = dataArr.append(df, ignore_index=True)
        if int(js[0]['count']) > pageNo * ct.OPEN_API_PAGE_NUM :
            pageNo = pageNo+1
            return _get_stock_hq_list(pageNo, dataArr)
        else:
            return dataArr
    except Exception as e:
        print(e)
        


def get_profit_data(year, quarter):
    """
        获取盈利能力数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
       
    Return
    --------
    DataFrame
        code,代码
        name,股票名称
        roe,净资产收益率（%）
        net_profit_ratio,净利率（%）
        net_profits,净利润（百万元）
        eps,每股收益（元）
        business_income,主营业务收入
        gross_profit_rate,毛利率（%）
        bips,每股主营业务收入（元）
    """
    if ct._check_input(year, quarter) is True:
        ct._write_head()
        data = _get_profit_data(year, quarter,1,pd.DataFrame())
        if data is not None and not data.empty:
            data = data.drop_duplicates('code')
            data['code'] = data['code'].map(lambda x:str(x).zfill(6))
        return data
    
def _get_profit_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["ylnl","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        ylnl_list_param = '["ylnl","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(ylnl_list_param,',[]')))
        request.add_header("User-Agent", ct.USER_AGENT)
        text = urlopen(request, timeout=ct.API_TIMEOUT).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'])
        if not df.empty:
            df = df.drop(0,axis=1)
            df.columns = ct.PROFIT_COLS
            dataArr = dataArr.append(df, ignore_index=True)
        if int(js[0]['count']) > pageNo * ct.OPEN_API_PAGE_NUM :
            pageNo = pageNo+1
            return _get_profit_data(year, quarter,pageNo, dataArr)
        else:
            return dataArr
    except Exception as e:
        print(e) 
    
def get_operation_data(year, quarter):
    """
        获取营运能力数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
       
    Return
    --------
    DataFrame
        code,代码
        name,股票名称
        arturnover,应收账款周转率（次）
        arturndays,应收账款周转天数（天）
        inventory_turnover,存货周转率（次）
        inventory_days,存货周转天数（天）
        currentasset_turnover,流动资产周转率（次）
        currentasset_days,流动资产周转天数（天）
    """
    if ct._check_input(year, quarter) is True:
        ct._write_head()
        data = _get_operation_data(year, quarter,1,pd.DataFrame())
        if data is not None and not data.empty:
            
            data = data.drop_duplicates('code')
            data['code'] = data['code'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_operation_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["yynl","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["yynl","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        request.add_header("User-Agent", ct.USER_AGENT)
        text = urlopen(request, timeout=ct.API_TIMEOUT).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'])
        if not df.empty:
            df = df.drop([3,4],axis=1)
            df.columns = ct.OPERATION_COLS
            dataArr = dataArr.append(df, ignore_index=True)
        if int(js[0]['count']) > pageNo * ct.OPEN_API_PAGE_NUM :
            pageNo = pageNo+1
            return _get_operation_data(year, quarter,pageNo, dataArr)
        else:
            return dataArr
    except Exception as e:
        print(e)
        
def get_growth_data(year, quarter):
    """
        获取成长能力数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
       
    Return
    --------
    DataFrame
        mbrg,主营业务收入增长率（%）
        nprg,净利润增长率（%）
        nav,净资产增长率（%）
        targ,总资产增长率（%）
        code,代码
        name,股票名称
        EXCHANGE,交易所
        eps,每股收益
        holderInterests,股东权益
        epsLastYear,去年每股收益
        holderInterestsLastYear,去年股东权益
        epsg,每股收益增长率（%）
        seg,股东权益增长率（%）
    """
    if ct._check_input(year, quarter) is True:

        ct._write_head()
        data = _get_growth_data(year, quarter,1,pd.DataFrame())

        if data is not None and not data.empty:
            data = data.drop_duplicates('code')
            data['code'] = data['code'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_growth_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["cnl","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["cnl","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        request.add_header("User-Agent", ct.USER_AGENT)
        text = urlopen(request, timeout=ct.API_TIMEOUT).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'])
        if not df.empty:
            df.columns=ct.GROWTH_COLS
            for col in (ct.GROWTH_COLS[0:4]+ct.GROWTH_COLS[7:]):
                df[col] = df[col].astype(str).replace("--","0").replace("", "0").replace("None","0").astype(float)
            dataArr = dataArr.append(df, ignore_index=True)
        if int(js[0]['count']) > pageNo * ct.OPEN_API_PAGE_NUM :
            pageNo = pageNo+1
            return _get_growth_data(year, quarter,pageNo, dataArr)
        else:
            return dataArr
    except Exception as e:
        print(e)


def get_debtpaying_data(year, quarter):
    """
        获取偿债能力数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
       
    Return
    --------
    DataFrame
        currentratio,流动比率（%）
        quickratio,速动比率（%）
        cashratio,现金比率（%）
        icratio,利息支付倍数
        sheqratio,股东权益比率（%）
        adratio,资产负债率（%）
        code,代码
        name,股票名称
    """
    
    #nocache
    if ct._check_input(year, quarter) is True:
        ct._write_head()
        data = _get_debtpaying_data(year, quarter,1,pd.DataFrame())
        if data is not None and not data.empty:
            data = data.drop_duplicates('code')
            data['code'] = data['code'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_debtpaying_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["cznl","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["cznl","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        request.add_header("User-Agent", ct.USER_AGENT)
        text = urlopen(request, timeout=ct.API_TIMEOUT).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'])
        if not df.empty:
            df = df.drop([5,6],axis=1)
            df.columns = ct.DEBTPAYING_COLS
            dataArr = dataArr.append(df, ignore_index=True)
        if int(js[0]['count']) > pageNo * ct.OPEN_API_PAGE_NUM :
            pageNo = pageNo+1
            return _get_debtpaying_data(year, quarter,pageNo, dataArr)
        else:
            return dataArr
    except Exception as e:
        print(e)

def get_cashflow_data(year, quarter):
    """
        获取现金流量数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
       
    Return
    --------
    DataFrame
        cf_sales,经营现金净流量对销售收入比率（%）
        rateofreturn,资产的经营现金流量回报率（%）
        cf_nm,经营现金净流量与净利润的比率（%）
        cf_liabilities,经营现金净流量对负债比率（%）
        cashflowratio,现金流量比率（%）
        code,代码
        name,股票名称
    """
    if ct._check_input(year, quarter) is True:
        ct._write_head()
        data = _get_cashflow_data(year, quarter,1,pd.DataFrame())
        if data is not None and not data.empty:
            data = data.drop_duplicates('code')
            data['code'] = data['code'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_cashflow_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["xjll","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["xjll","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        request.add_header("User-Agent", ct.USER_AGENT)
        text = urlopen(request, timeout=ct.API_TIMEOUT).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'])
        if not df.empty:
            df.columns = ct.CASHFLOW_COLS
            dataArr = dataArr.append(df, ignore_index=True)
        if int(js[0]['count']) > pageNo * ct.OPEN_API_PAGE_NUM :
            pageNo = pageNo+1
            return _get_cashflow_data(year, quarter,pageNo, dataArr)
        else:
            return dataArr
    except Exception as e:
        print(e)

def get_report_data(year, quarter):
    """
        获取业绩报表数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
       
    Return
    --------
    DataFrame
        eps,每股收益（元）
        bvps,每股净资产（元）
        roe,净资产收益率（%）
        epcf,每股现金流量（元）
        net_profits,净利润（万元）
        code,代码
        name,股票名称
        exchange,交易所
        epslastyear,去年同期每股收益
        netprofitlastyear,去年同期净利润
        eps_yoy,每股收益同比（%）
        profits_yoy,净利润同比（%）
        distrib,利润分配方案
        detail,详情
    """
    if ct._check_input(year, quarter) is True:
        
        ct._write_head()
        data = _get_report_data(year, quarter,1,pd.DataFrame())
        if data is not None and not data.empty:
            data = data.drop_duplicates('code')
            data['code'] = data['code'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_report_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["xjll","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["yjbb","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        request.add_header("User-Agent", ct.USER_AGENT)
        text = urlopen(request, timeout=ct.API_TIMEOUT).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'])
        if not df.empty:
            df = df.drop([0,2],axis=1)
            df.columns = ct.REPORT_COLS
            dataArr = dataArr.append(df, ignore_index=True)
        if int(js[0]['count']) > pageNo * ct.OPEN_API_PAGE_NUM :
            pageNo = pageNo+1
            return _get_report_data(year, quarter,pageNo, dataArr)
        else:
            return dataArr
    except Exception as e:
        print(e)
if __name__ == '__main__':
    data = get_growth_data(2015,2)
    print data
    '''
    
    data = get_stock_hq_list()
    print data
    
    data = get_profit_data(2015,2)
    print data
    
    data = get_operation_data(2015,2)
    print data
    
    data = get_growth_data(2015,2)
    print data
    
    data = get_debtpaying_data(2015,2)
    print data
    
    data = get_report_data(2015,2)
    print data
    '''
    


