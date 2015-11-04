# coding: utf-8


import pandas as pd


class BaseTechnical:
    stockData = pd.DataFrame()
    dataIndexOpen  = "Open"   #开盘价
    dataIndexClose = "Close"  #收盘价
    dataIndexHigh  = "High"   #最高价
    dataIndexLow   = "Low"    #最低价
    dataIndexVol   = "Vol"    #成交量
    
    def __init__(self,stock_data):
        assert(isinstance(stock_data, pd.DataFrame))
        self.stockData = stock_data
        
    def HHV(self,data_index,cycle):
        
        dataList = range(self.stockData[data_index].size)
        tmpList = []
        
        for item in dataList:
            # 防止前day沒有data
            if cycle == 0:
                tmp = self.stockData[data_index][item:].max()
            elif item+cycle < self.stockData[data_index].size:
                tmp = self.stockData[data_index][item:item+cycle].max()
            else:
                tmp = self.stockData[data_index][item:].max()
        tmpList.append(tmp)
        
        tmpSeries = pd.Series(tmpList)   
        self.stockData["HHV"+str(cycle)] = tmpSeries
        return self.stockData["HHV"+str(cycle)]
    
    def LLV(self,data_index,cycle):
        
        dataList = range(self.stockData[data_index].size)
        tmpList = []
        
        for item in dataList:
            # 防止前day沒有data
            if cycle == 0:
                tmp = self.stockData[data_index][item:].max()
            elif item+cycle < self.stockData[data_index].size:
                tmp = self.stockData[data_index][item:item+cycle].min()
            else:
                tmp = self.stockData[data_index][item:].min()
        tmpList.append(tmp)
        
        tmpSeries = pd.Series(tmpList)   
        self.stockData["LLV"+str(cycle)] = tmpSeries
        return self.stockData["LLV"+str(cycle)]
        
    def MA(self,data_index,cycle):
        
        assert(cycle>0)
        dataList = range(self.stockData[data_index].size)
        tmpList = []
        
        for item in dataList:
            # 防止前day沒有data
            if item+cycle < self.stockData[data_index].size:
                # 移动平均数= 采样天数的股价合计 / 采样天数
                # [item-day+1:item+1] 当前日子区间
                tmp = self.stockData[data_index][item:item+cycle].mean()
                tmpList.append(tmp)
            
        tmpSeries = pd.Series(tmpList)   
        self.stockData["MA"+str(cycle)] = tmpSeries
        return self.stockData["MA"+str(cycle)]
    
    def REF(self,data_index,cycle):
        dataList = range(self.stockData[data_index].size)
        tmpList = []
        
        for item in dataList:
            # 防止前day沒有data
            if item+cycle < self.stockData[data_index].size:
                # 移动平均数= 采样天数的股价合计 / 采样天数
                # [item-day+1:item+1] 当前日子区间
                tmp = self.stockData[data_index][item+cycle]
                tmpList.append(tmp)
        tmpSeries = pd.Series(tmpList)   
        self.stockData["REF"+str(cycle)] = tmpSeries
        return self.stockData["REF"+str(cycle)]
    
    
    
    
    
    def CROSS(self,data_index_a,data_index_b):

        dataList = range(1,self.stockData[data_index_a].size)
        
        tmpList = []
        
        for item in dataList:
            if (self.stockData[data_index_a][item-1] > self.stockData[data_index_b][item-1] 
                and self.stockData[data_index_b][item] < self.stockData[data_index_b][item]
                ):
                tmpList.append(True)
            else:
                tmpList.append(False)
        tmpSeries = pd.Series(tmpList)
        self.stockData["CROSS_"+str(data_index_a)+"_"+str(data_index_b)] = tmpSeries
        return self.stockData["CROSS_"+str(data_index_a)+"_"+str(data_index_b)]
    
    def BARSLAST(self,data_index):

        dataList = range(0,self.stockData[data_index].size)
        dataList.reverse()
        
        tmpList = []
        for item in dataList:
            if(self.stockData[data_index][item] == False):
                #从第二个值开始计数
                if len(tmpList)>0 and tmpList[-1] != -1:
                    tmpList.append(tmpList[-1]+1)
                else:
                    tmpList.append(-1)
            else:
                tmpList.append(0)
        tmpList.reverse()
        tmpSeries = pd.Series(tmpList)
        self.stockData["barslast"+str(data_index)] = tmpSeries
        return self.stockData["barslast"+str(data_index)]