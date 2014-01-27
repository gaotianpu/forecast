#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
from config import dbr,dbw
import comm

def getFutureRange(prate):
    if prate>10:  #1%
        return 2
    if prate<=10:
        return 1
    return 0

    # if prate < -20: #-2%
    #     return 1 
    # if prate<=10 and prate>=-20:
    #     return 2
    # return 0    

def computeFuture(records):
    for r in records:
        i = records.index(r)        
        if i>1:
            prate = int((records[i-2].close - records[i-1].close) *1000 / records[i-1].close)
            frange = getFutureRange(prate)
            sql = 'update stock_daily set future1_prate=%s,future1_range=%s where pk_id=%s' % (prate,frange,r.pk_id) 
            dbw.query(sql)
        if i>2:
            prate = int((records[i-3].close - records[i-1].close) *1000 / records[i-1].close )
            frange = getFutureRange(prate)
            sql = 'update stock_daily set future2_prate=%s,future2_range=%s where pk_id=%s' % (prate,frange,r.pk_id)  
            dbw.query(sql)            
        if i>3:
            prate = int((records[i-4].close - records[i-1].close) *1000 / records[i-1].close )
            frange = getFutureRange(prate)
            sql = 'update stock_daily set future3_prate=%s,future3_range=%s where pk_id=%s' % (prate,frange,r.pk_id) 
            dbw.query(sql)

def computeTrend(records):
    count = len(records)
    for i in range(0,count):        
        if count-i>2:
            t3 = comm.get_trend(records[i:i+3])
            sql = 'update stock_daily set trend_3=%s where pk_id=%s' % (t3,records[i].pk_id) 
            dbw.query(sql)
        if count-i>4:
            t5 = comm.get_trend(records[i:i+5])
            sql = 'update stock_daily set trend_5=%s where pk_id=%s' % (t5,records[i].pk_id) 
            dbw.query(sql) 
             
def run_all():
    stocks = da.stockbaseinfos.load_all_stocks()  
    for s in stocks:         
        stock_daily_records = da.stockdaily.load_stockno(s.stock_no)
        computeFuture(stock_daily_records)
        #computeTrend(stock_daily_records)


if __name__ == '__main__':
    run_all()