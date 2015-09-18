# -*- coding:utf-8 -*- 
"""
基本面数据接口 
Created on 2015/09/09
@author: Jacob He
@contact: hezhenke123@163.com
"""
import pandas as pd
import cons as ct
import cache
import lxml.html
from lxml import etree
import re
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
    if df is not None:
        df = df.drop_duplicates('code')
        df['code'] = df['code'].map(lambda x:str(x).zfill(6))
    return df
def _get_stock_hq_list(pageNo, dataArr):
    ct._write_console()
    try:
        #param:["hq","hs_a","{sort}",{asc},{page},{num}]
        hq_list_param = '["hq","hs_a","",0,%d,%d]'%(pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(hq_list_param,',[]')))
        text = urlopen(request, timeout=10).read()
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
        Symbol,代码
        SName,股票名称
        JZCSYL,净资产收益率（%）
        NPMargin,净利率（%）
        JLR,净利润（百万元）
        MGSY,每股收益（元）
        ZYYWSR,主营业务收入
        myGPMargin,毛利率（%）
        SPS,每股主营业务收入（元）
    """
    if ct._check_input(year, quarter) is True:
        ct._write_head()
        data = _get_profit_data(year, quarter,1,pd.DataFrame())
        if data is not None:
            data = data.drop('PTROA',axis=1)
            data = data.drop_duplicates('Symbol')
            data['Symbol'] = data['Symbol'].map(lambda x:str(x).zfill(6))
        return data
    
def _get_profit_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["ylnl","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        ylnl_list_param = '["ylnl","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(ylnl_list_param,',[]')))
        text = urlopen(request, timeout=10).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'], columns=js[0]['fields'])
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
        Symbol,代码
        SName,股票名称
        FinancialRatios3,应收账款周转率（次）
        inancialRatios4,应收账款周转天数（天）
        FinancialRatios19,存货周转率（次）
        FinancialRatios22,存货周转天数（天）
        FinancialRatios24,流动资产周转率（次）
        FinancialRatios25,流动资产周转天数（天）
    """
    if ct._check_input(year, quarter) is True:
        ct._write_head()
        data = _get_operation_data(year, quarter,1,pd.DataFrame())
        if data is not None:
            data = data.drop('FinancialRatios21',axis=1)
            data = data.drop('FinancialRatios23',axis=1)
            data = data.drop_duplicates('Symbol')
            data['Symbol'] = data['Symbol'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_operation_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["yynl","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["yynl","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        
        text = urlopen(request, timeout=10).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'], columns=js[0]['fields'])
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
        filename = "growth_data_%d_%d.csv"%(year, quarter)
        data = cache.read_cache(filename)
        if  data is not None:
            data = data.drop_duplicates('code')
            data['code'] = data['code'].map(lambda x:str(x).zfill(6))
            return data
        #nocache
        ct._write_head()
        data = _get_growth_data(year, quarter,1,pd.DataFrame())
        cache.write_cache(data,filename)
        if data is not None:
            data = data.drop_duplicates('code')
            data['code'] = data['code'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_growth_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["cnl","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["cnl","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        
        text = urlopen(request, timeout=10).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'],columns=ct.GROWTH_COLS)
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
        FinancialRatios1,流动比率（%）
        FinancialRatios2,速动比率（%）
        FinancialRatios5,现金比率（%）
        FinancialRatios6,利息支付倍数
        FinancialRatios8,股东权益比率（%）
        FinancialRatios56,资产负债率（%）
        Symbol,代码
        SName,股票名称
    """
    
    #nocache
    if ct._check_input(year, quarter) is True:
        filename = "debtpaying_data_%d_%d.csv"%(year, quarter)
        data = cache.read_cache(filename)
        if  data is not None:
            return data
        ct._write_head()
        data = _get_debtpaying_data(year, quarter,1,pd.DataFrame())
        if data is not None:
            data = data.drop('FinancialRatios9',axis=1)
            data = data.drop('FinancialRatios18',axis=1)
            data = data.drop_duplicates('Symbol')
            data['Symbol'] = data['Symbol'].map(lambda x:str(x).zfill(6))
        cache.write_cache(data,filename)
        return data
        
def _get_debtpaying_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["cznl","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["cznl","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        
        text = urlopen(request, timeout=10).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'], columns=js[0]['fields'])
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
        FinancialRatios47,经营现金净流量对销售收入比率（%）
        FinancialRatios48,资产的经营现金流量回报率（%）
        FinancialRatios49,经营现金净流量与净利润的比率（%）
        FinancialRatios50,经营现金净流量对负债比率（%）
        FinancialRatios51,现金流量比率（%）
        Symbol,代码
        SName,股票名称
    """
    if ct._check_input(year, quarter) is True:
        ct._write_head()
        data = _get_cashflow_data(year, quarter,1,pd.DataFrame())
        if data is not None:
            data = data.drop_duplicates('Symbol')
            data['Symbol'] = data['Symbol'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_cashflow_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["xjll","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["xjll","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        
        text = urlopen(request, timeout=10).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'], columns=js[0]['fields'])
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
        CompanyCode,公司代码
        ReportDate,报告时间
        PUBLISHDATE,报告实际发布时间
        eps,每股收益（元）
        MFRatio18,每股净资产（元）
        MFRatio22,净资产收益率（%）
        MFRatio20,每股现金流量（元）
        MFRatio2,净利润（万元）
        Symbol,代码
        SName,股票名称
        EXCHANGE,交易所
        epsLastYear,去年同期每股收益
        netprofitLastYear,去年同期净利润
        eps_ratio,每股收益同比（%）
        MFRatio2Ratio,净利润同比（%）
        DisHty,利润分配方案
        detail,详情
    """
    if ct._check_input(year, quarter) is True:
        
        ct._write_head()
        data = _get_report_data(year, quarter,1,pd.DataFrame())
        if data is not None:
            data = data.drop_duplicates('Symbol')
            data['Symbol'] = data['Symbol'].map(lambda x:str(x).zfill(6))
        return data
        
def _get_report_data(year, quarter,pageNo,dataArr):
    ct._write_console()
    try:

        #param:["xjll","行业","地域","概念","年","季度","{sort}",{asc},{page},{num}]
        list_param = '["yjbb","","","","%d","%d","",0,%d,%d]'%(year, quarter,pageNo,ct.OPEN_API_PAGE_NUM)
        request = Request(ct.SINA_OPEN_API_URL%(quote(list_param,',[]')))
        
        text = urlopen(request, timeout=10).read()
        text = text.decode('gbk') if ct.PY3 else text 
        js = json.loads(text.strip())
        if js is None:
            return dataArr
        df = pd.DataFrame(js[0]['items'], columns=js[0]['fields'])
        dataArr = dataArr.append(df, ignore_index=True)
        if int(js[0]['count']) > pageNo * ct.OPEN_API_PAGE_NUM :
            pageNo = pageNo+1
            return _get_report_data(year, quarter,pageNo, dataArr)
        else:
            return dataArr
    except Exception as e:
        print(e)
if __name__ == '__main__':
    
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
    
    


