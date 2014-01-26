#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
from config import dbr,dbw

def run(stock_no):   
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
             
    

if __name__ == '__main__':
    run('300233')