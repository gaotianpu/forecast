#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import config
import numpy

def load_stock_history(stock_no):
    #return 0.Date 1.Open  2.High  3.Low   4.Close 5.Volume  6.AdjClose
    records = []
    lfile = '%s%s.csv' %(config.history_data_dir,stock_no)
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close()
        for l in lines[1:] :
            items = l.strip().split(',')
            items[1] = float(items[1])
            items[2] = float(items[2])
            items[3] = float(items[3])
            items[4] = float(items[4])
            items[5] = int(items[5])
            items[6] = float(items[6])            
            if items[5]!='000':                
                records.append(items)            
    return records


def load_daily_stocks(date):       
    lfile = '%s%s.csv' %(config.daily_data_dir,date)
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close()

    d = {} 
    for l in lines:
        fields=l.strip().split(',')
        print fields
        #get stock_no
        d[fields[0]] = fields    
    return d


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

#统计过去一年的成交量分布情况
def compute_Volume(stock_no,days):
    records = load_stock_history(stock_no)
    Volumes = [r[5] for r in records[:days]]
    narray = numpy.array(Volumes) 
    print narray.mean(), narray.var(), narray.std() #均值,方差,标准差
    


if __name__ == "__main__" : 
    load_daily_stocks('2015-03-23')
    # compute_Volume('600000.ss',300)   
    # price_change_rate('600000.ss',3)