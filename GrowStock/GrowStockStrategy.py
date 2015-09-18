#-*- coding: UTF-8 -*-

"""
获取股票分类数据接口

成长股追踪策略

1.选股篇
一,最近三年公司缓慢增长或增速下降、不增反降、甚至亏损
二,最近三个季度快速增长或增速加快、业绩拐点、扭亏为盈
三,公司总市值不大
四,必须是朝阳行业,比如生物制药、电子科技、环保、能源、消费等
五,新闻事件发生,比如股权激励、公司回购、更换高管、业绩预增、收购兼并等
六,开始有机构跟踪分析



2.追踪买入篇
股价总体是在长周期的底部,市净率不高
图形上形成带柄茶壶、股价上突破关键价格突破前有缩量十字星、突破时放巨量最好

3.卖出篇

仓位控制:分批建仓,从观察仓、到正式仓分为普通舱、头等舱,个股不大于总仓位的30%
卖出设置:如果判断失误立即止损上涨最厉害时,主动收回成本。


Created on 2015/08/20
@author: jacob he
@group : AshareQuant
@contact: hezenke123@163.com
"""


import os,sys
import datetime
import pandas as pd
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from lib.util import WrapperTushare

def get_stock_growth():
    """
        获取股票3年的增长率和最近几个季度的增长率
    Return
    --------
    DataFrame
        code :股票代码
        name :股票名称
        1year:最近一年增长率
        2year:最近二年增长率
        3year:最近三年增长率
        4year:最近四年增长率
        1quarter:最近一季度增长率
        2quarter:最近二季度增长率
        3quarter:最近三季度增长率
        4quarter:最近四季度增长率
    """
    myts = WrapperTushare()
    stock_list = myts.get_stock_basics()
    df = pd.DataFrame(index=stock_list.index, columns=['name','industry','area','1quarter','2quarter','1year','2year','3year','4year','3quarter','4quarter'])
    df['name'] = stock_list['name']
    df['industry'] = stock_list['industry']
    df['area'] = stock_list['area']
    cur = datetime.datetime.now()
    curyear = cur.year
    fir_year_growth_data = myts.get_growth_data(curyear-1,4)
    if fir_year_growth_data.empty:
        curyear = curyear - 1
        fir_year_growth_data = myts.get_growth_data(curyear-1,4)
    sec_year_growth_data = myts.get_growth_data(curyear-2,4)
    thir_year_growth_data = myts.get_growth_data(curyear-3,4)
    for_year_growth_data = myts.get_growth_data(curyear-4,4)

    for i in fir_year_growth_data.index:
        df.loc[fir_year_growth_data.loc[i,'code'],'1year'] = fir_year_growth_data.loc[i,'nprg']
    for i in sec_year_growth_data.index:
        df.loc[sec_year_growth_data.loc[i,'code'],'2year'] = sec_year_growth_data.loc[i,'nprg']
    for i in thir_year_growth_data.index:
        df.loc[thir_year_growth_data.loc[i,'code'],'3year'] = thir_year_growth_data.loc[i,'nprg']
    for i in for_year_growth_data.index:
        df.loc[for_year_growth_data.loc[i,'code'],'4year'] = for_year_growth_data.loc[i,'nprg']

    curmonth = cur.month
    if curmonth in(4,5,6):
        curquarter = 1
        curyear = cur.year
    elif curmonth in (7,8,9):
        curquarter = 2
        curyear = cur.year
    elif curmonth in (10,11,12):
        curquarter = 3
        curyear = cur.year
    elif curmonth in(1,2,3):
        curquarter = 4
        curyear = cur.year - 1
    fir_quarter_growth_data = myts.get_growth_data(curyear,curquarter)
    if fir_quarter_growth_data.empty:
        curyear,curquarter = _sub_quarter(curyear,curquarter)
        fir_quarter_growth_data = myts.get_growth_data(curyear,curquarter)
    curyear2,curquarter2 = _sub_quarter(curyear,curquarter)
    sec_quarter_growth_data = myts.get_growth_data(curyear2,curquarter2)

    curyear3,curquarter3 = _sub_quarter(curyear2,curquarter2)
    thir_quarter_growth_data = myts.get_growth_data(curyear3,curquarter3)

    curyear4,curquarter4 = _sub_quarter(curyear3,curquarter3)
    for_quarter_growth_data = myts.get_growth_data(curyear4,curquarter4)

    for i in fir_quarter_growth_data.index:
        df.loc[fir_quarter_growth_data.loc[i,'code'],'1quarter'] = fir_quarter_growth_data.loc[i,'nprg']
    for i in sec_quarter_growth_data.index:
        df.loc[sec_quarter_growth_data.loc[i,'code'],'2quarter'] = sec_quarter_growth_data.loc[i,'nprg']
    for i in thir_quarter_growth_data.index:
        df.loc[thir_quarter_growth_data.loc[i,'code'],'3quarter'] = thir_quarter_growth_data.loc[i,'nprg']
    for i in for_quarter_growth_data.index:
        df.loc[for_quarter_growth_data.loc[i,'code'],'4quarter'] = for_quarter_growth_data.loc[i,'nprg']
    return df

    
def _sub_quarter(curyear,curquarter):
    if curquarter == 1:
        curquarter = 4
        curyear = curyear - 1
    else:
        curquarter = curquarter - 1
    return curyear,curquarter

def run_strategy():
    df = get_stock_growth()
    df['1year'] = df['1year'].replace('--','0').astype(float)
    df['2year'] = df['2year'].replace('--','0').astype(float)
    df['3year'] = df['3year'].replace('--','0').astype(float)
    df['4year'] = df['4year'].replace('--','0').astype(float)

    df['1quarter'] = df['1quarter'].replace('--','0').astype(float)
    df['2quarter'] = df['2quarter'].replace('--','0').astype(float)
    df['3quarter'] = df['3quarter'].replace('--','0').astype(float)
    df['4quarter'] = df['4quarter'].replace('--','0').astype(float)

    df2= df[(df['1year']<30)&(df['2year']<30)&(df['3year']<30)]
    df_strong = df2[(df['1quarter']>30)|(df['2quarter']>30)&(df['3quarter']>30)]
    df_strong = df_strong.sort(['industry', '1quarter'], ascending=[1, 0])
    return df_strong
if __name__ == '__main__':
    df = run_strategy()
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data','result.csv')
    df.to_csv(file_path, encoding='utf-8')
