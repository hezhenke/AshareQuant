# -*- coding:utf-8 -*-
"""
Created on 2015/09/11
@author: Jacob He
@contact: hezhenke123@163.com
"""

VERSION = '0.1.0'

DOMAINS = {'sinaapi': 'money.finance.sina.com.cn', 'sinahq': 'sinajs.cn',}
PAGES = {'openapi': 'openapi_proxy.php'}
P_TYPE = {'http': 'http://', 'ftp': 'ftp://'}
PAGE_NUM = [1, 40, 80, 100,100]

#fundamental
#param:"[%22hq%22,%22hs_a%22,%22{sort}%22,{asc},{page},{num}]"
SINA_OPEN_API_URL = "http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[%s]"
OPEN_API_PAGE_NUM = 100
PROFIT_COLS = ['roe', 'net_profit_ratio','net_profits','eps','business_income','gross_profit_rate', 'bips', 'code', 'name']
OPERATION_COLS = ['arturnover', 'arturndays', 'inventory_turnover','inventory_days', 'currentasset_turnover', 'currentasset_days','code', 'name']
GROWTH_COLS = ['mbrg', 'nprg', 'nav', 'targ', 'code', 'name', 'exchage','eps','holderInterests','epsLastYear','holderInterestsLastYear','epsg', 'seg']
DEBTPAYING_COLS = ['currentratio','quickratio', 'cashratio', 'icratio', 'sheqratio', 'adratio','code', 'name']
CASHFLOW_COLS = ['cf_sales', 'rateofreturn','cf_nm', 'cf_liabilities', 'cashflowratio','code', 'name']
REPORT_COLS = ['report_date','eps', 'bvps', 'roe','epcf', 'net_profits', 'code', 'name','exchange','epslastyear','netprofitlastyear','eps_yoy','profits_yoy', 'distrib', 'detail']
API_TIMEOUT = 50
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"

#tading price
DAY_PRICE_MIN_URL = 'http://api.finance.ifeng.com/akmin?scode=%s&type=%s'
DAY_PRICE_URL = 'http://api.finance.ifeng.com/%s/?code=%s&type=last'
SINA_DAY_PRICE_URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?num=80&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page&page=%s'
TICK_PRICE_URL = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s'
TODAY_TICKS_PAGE_URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date=%s&symbol=%s'
TODAY_TICKS_URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=%s&date=%s&page=%s'
LIVE_DATA_URL = 'http://hq.sinajs.cn/rn=%s&list=%s'
HIST_FQ_FACTOR_URL = 'http://vip.stock.finance.sina.com.cn/api/json.php/BasicStockSrv.getStockFuQuanData?symbol=%s&type=hfq'
INDEX_HQ_URL = '''http://hq.sinajs.cn/rn=xppzh&list=sh000001,sh000002,sh000003,sh000008,sh000009,sh000010,sh000011,sh000012,sh000016,sh000017,sh000300,sz399001,sz399002,sz399003,sz399004,sz399005,sz399006,sz399100,sz399101,sz399106,sz399107,sz399108,sz399333,sz399606'''
HIST_FQ_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/%s.phtml?year=%s&jidu=%s'
HIST_INDEX_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s/type/S.phtml?year=%s&jidu=%s'

K_LABELS = ['D', 'W', 'M']
K_MIN_LABELS = ['5', '15', '30', '60']
K_TYPE = {'D': 'akdaily', 'W': 'akweekly', 'M': 'akmonthly'}
INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb']
INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sz399300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006'}
DAY_PRICE_COLUMNS = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
                     'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover']
INX_DAY_PRICE_COLUMNS = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
                         'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20']
LIVE_DATA_COLS = ['name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount',
                  'b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p',
                  'a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v', 'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p', 'date', 'time', 's']
TICK_COLUMNS = ['time', 'price', 'change', 'volume', 'amount', 'type']
TODAY_TICK_COLUMNS = ['time', 'price', 'pchange', 'change', 'volume', 'amount', 'type']
DAY_TRADING_COLUMNS = ['code', 'symbol', 'name', 'changepercent',
                       'trade', 'open', 'high', 'low', 'settlement', 'volume', 'turnoverratio']
HIST_FQ_COLS = ['date', 'open', 'high', 'close', 'low', 'volume', 'amount', 'factor']
INDEX_HEADER = 'code,name,open,preclose,close,high,low,0,0,volume,amount,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,d,c,3\n'
INDEX_COLS = ['code', 'name', 'change', 'open', 'preclose', 'close', 'high', 'low', 'volume', 'amount']
FORMAT = lambda x: '%.2f' % x

#console
DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'
DATA_ROWS_TIPS = '%s rows data found.Please wait for a moment.'
DATA_INPUT_ERROR_MSG = 'date input error.'
NETWORK_URL_ERROR_MSG = '获取失败，请检查网络和URL'
DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'
TOP_PARAS_MSG = 'top有误，请输入整数或all.'
LHB_MSG = '周期输入有误，请输入数字5、10、30或60'

#MYSQL
MYSQLDB_HOST = '127.0.0.1'
MYSQLDB_USER = 'root'
MYSQLDB_PASS = 'root'
MYSQLDB_DATABASE = 'stock'
MYSQLDB_CHARSET = 'utf8'

#mongo
MONGO_DATABASE = 'stock2'
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

import sys
PY3 = (sys.version_info[0] >= 3)
def _write_head():
    sys.stdout.write(DATA_GETTING_TIPS)
    sys.stdout.flush()

def _write_console():
    sys.stdout.write(DATA_GETTING_FLAG)
    sys.stdout.flush()
    
def _write_tips(tip):
    sys.stdout.write(DATA_ROWS_TIPS%tip)
    sys.stdout.flush()

def _write_msg(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()
    
def _check_input(year, quarter):
    if isinstance(year, str) or year < 1989 :
        raise TypeError(DATE_CHK_MSG)
    elif quarter is None or isinstance(quarter, str) or quarter not in [1, 2, 3, 4]:
        raise TypeError(DATE_CHK_Q_MSG)
    else:
        return True
    
def _check_lhb_input(last):
    if last not in [5, 10, 30, 60]:
        raise TypeError(LHB_MSG)
    else:
        return True
