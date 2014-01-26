#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
from config import dbr,dbw

def compute_one_stock(stock_no):   
    records = da.stockdaily.load_stockno(stock_no)
    for r in records:
        i = records.index(r)        
        if i>1:
            prate = int((records[i-2].close - records[i-1].close) / records[i-1].close*100)
            sql = 'update stock_daily set future1_prate=%s where pk_id=%s' % (prate,r.pk_id) 
            dbw.query(sql)
        if i>2:
            prate = int((records[i-3].close - records[i-1].close) / records[i-1].close*100)
            sql = 'update stock_daily set future2_prate=%s where pk_id=%s' % (prate,r.pk_id)  
            dbw.query(sql)            
        if i>3:
            prate = int((records[i-4].close - records[i-1].close) / records[i-1].close*100)
            sql = 'update stock_daily set future3_prate=%s where pk_id=%s' % (prate,r.pk_id) 
            dbw.query(sql)
             
def run_all():
    stocks = da.stockbaseinfos.load_all_stocks() #[web.storage(stock_no='000001',pk_id=332)] #test
    for s in stocks:
        compute_one_stock(s.stock_no)    

if __name__ == '__main__':
    run_all()