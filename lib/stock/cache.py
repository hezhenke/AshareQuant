# -*- coding:utf-8 -*- 
"""
缓存工具 
Created on 2015/09/16
@author: Jacob He
@contact: hezhenke123@163.com
"""
import pandas as pd
import os

def write_cache(df,fileName):
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'data','cache',fileName)
    if isinstance(df, pd.DataFrame):
        df.to_csv(file_path,index=False,encoding='utf-8')
    else:
        raise RuntimeError('data type is incorrect')
    

def read_cache(fileName):
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'data','cache',fileName)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        return None
    
