#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
from config import dbr,dbw

def getFutureRange(prate):
    if prate>10:  #1%
        return 3
    if prate < -20: #-2%
        return 1 
    if prate<=10 and prate>=-20:
        return 2
    return 0
    

def compute_one_stock(stock_no):   
    records = da.stockdaily.load_stockno(stock_no)
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
             
def run_all():
    stocks = da.stockbaseinfos.load_all_stocks()  
    for s in stocks:
        compute_one_stock(s.stock_no)    

if __name__ == '__main__':
    run_all()