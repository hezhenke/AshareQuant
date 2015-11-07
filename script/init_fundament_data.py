# -*- coding:utf-8 -*-
"""
Created on 2015/09/30
@author: Jacob He
@contact: hezhenke123@163.com
"""
from lib.stock.DbCache import DbCache

if __name__ == '__main__':
    #init the fundament data
    c = DbCache()
    c.check_db_cache(1989)
