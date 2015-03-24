#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import numpy
import web
import config

def load_stock_history(stock_no):    
    records = []
    lfile = '%s%s.csv' %(config.history_data_dir,stock_no)
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close()
        for l in lines[1:] :
            items = l.strip().split(',')
            if items[5]=='000': continue
            #0.Date 1.Open  2.High  3.Low   4.Close 5.Volume  6.AdjClose
            r = web.storage(date=items[0],open=float(items[1]),high=float(items[2]),
                low=float(items[3]),close=float(items[4]),
                volume=float(items[5]),adjclose=float(items[6]))                                        
            records.append(r)            
    return records


def load_daily_stocks(date):       
    lfile = '%s%s.csv' %(config.daily_data_dir,date)
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close()
        
    d = {} 
    for l in lines:
        items=l.strip().split(',')        
        r = web.storage(
            open=float(items[1]),
            last_close=float(items[2]),
            close=float(items[3]),
            high=float(items[4]),
            low=float(items[5]),
            volume=float(items[6]),
            amount=float(items[7]),
            date=items[8],                
            time=items[9])   
        d[items[0]] = r    
    return d

# 1：”27.55″，今日开盘价；
# 2：”27.25″，昨日收盘价；
# 3：”26.91″，当前价格；
# 4：”27.55″，今日最高价；
# 5：”26.20″，今日最低价；
# 6：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
# 7：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
# 8：”2008-01-11″，日期；
# 9：”15:05:32″，时间；

#a = today_close_price
#b = (today-n_day)_open_price
#经济学价格变化率：(a-b)/((a+b)/2)
def price_change_rate(stock_no,days):
    l = []
    records = load_stock_history(stock_no)
    count = len(records)
    for i in range(0,count-days):
        a =  records[i][4]
        b =  records[i+days][1]       
        prate = (a-b)/((a+b)/2)
        l.append((records[i][0],int(prate*100)))
        # print records[i][0],records[i][1],records[i][4],int(prate*100)
    return l
    # print float(len([i for i in l if i[1]>1]))/len(l)

#统计过去days天的成交量分布情况
def compute_Volume(stock_no,days):
    records = load_stock_history(stock_no)
    Volumes = [r[5] for r in records[:days]]
    narray = numpy.array(Volumes) 
    print narray.mean(), narray.var(),narray.std() #均值,方差,标准差
    


if __name__ == "__main__" : 
    # load_stock_history('600000.ss')
    load_daily_stocks('2015-03-23')
    # compute_Volume('600000.ss',300)   
    # price_change_rate('600000.ss',3)

