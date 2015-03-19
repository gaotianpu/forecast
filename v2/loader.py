#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import config

def load_stock_history(stock_no):
    #return 0.Date 1.Open  2.High  3.Low   4.Close 5.Volume  6.AdjClose
    records = []
    lfile = '%s%s.csv' %(config.history_data_dir,stock_no)
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close()
        for l in lines[1:] :
            items = l.strip().split(',')
            if items[5]!='000':                
                records.append(items)            
    return records

#a = today_close_price
#b = (today-n_day)_open_price
#经济学价格变化率：(a-b)/((a+b)/2)
def price_change_rate(stock_no,days):
    l = []
    records = load_stock_history(stock_no)
    count = len(records)
    for i in range(0,count-days):
        a =  float(records[i][4])
        b =  float(records[i+days][1])        
        prate = (a-b)/((a+b)/2)
        l.append((records[i][0],int(prate*100)))
        # print records[i][0],records[i][1],records[i][4],int(prate*100)
    return l
    # print float(len([i for i in l if i[1]>1]))/len(l)
    


if __name__ == "__main__" :    
    price_change_rate('600000.ss',3)