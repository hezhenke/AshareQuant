# -*- coding:utf-8 -*-
"""
Created on 2015/09/28
@author: Jacob He
@contact: hezhenke123@163.com
"""

from lib.util.StoreMysql import store_all_data_to_mysql


#获取业绩报表
store_all_data_to_mysql("get_report_data","report_data")

#获取盈利数据
store_all_data_to_mysql("get_profit_data","profit_data")

#获取营运能力数据
store_all_data_to_mysql("get_operation_data","operation_data")


#获取成长能力数据
store_all_data_to_mysql("get_growth_data","growth_data")

#获取偿债能力数据
store_all_data_to_mysql("get_debtpaying_data","debtpaying_data")

#获取偿债能力数据
store_all_data_to_mysql("get_cashflow_data","cashflow_data")
