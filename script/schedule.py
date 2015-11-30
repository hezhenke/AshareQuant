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

import check_mongo_hist_data

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request




if __name__ == '__main__':
    
    #更新基本面数据 
    
    cur = datetime.now()
    curyear = cur.year
    c = DbCache()
    c.check_db_cache(curyear)
    
    #更新历史数据
    check_mongo_hist_data.run()
    
    
    