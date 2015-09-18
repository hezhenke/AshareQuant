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
#param:"[%22hq%22,%22hs_a%22,%22{sort}%22,{asc},{page},{num}]"
SINA_OPEN_API_URL = "http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[%s]"
OPEN_API_PAGE_NUM = 100
GROWTH_COLS = ['mbrg', 'nprg', 'nav', 'targ', 'code', 'name', 'exchage','eps','holderInterests','epsLastYear','holderInterestsLastYear','epsg', 'seg']

DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'
DATA_ROWS_TIPS = '%s rows data found.Please wait for a moment.'
DATA_INPUT_ERROR_MSG = 'date input error.'
NETWORK_URL_ERROR_MSG = '获取失败，请检查网络和URL'
DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'
TOP_PARAS_MSG = 'top有误，请输入整数或all.'
LHB_MSG = '周期输入有误，请输入数字5、10、30或60'

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
