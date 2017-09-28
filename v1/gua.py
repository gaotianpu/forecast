#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
import da

def update(pkid,gua64):
    dbw.update('stock_base_infos',
        gua64=gua64,         
        where="pk_id=$pkid",vars=locals())

def update_daily(stock_no,date,gua64):
    dbw.update('stock_daily_records',
        gua64=gua64,         
        where="stock_no=$stock_no and date=$date",vars=locals())

#8卦，64卦
def run():
    stocks = da.stockbaseinfos.load_all_stocks() #[web.storage(stock_no='000001',pk_id=332)] #test
    for s in stocks:
        r3 = da.dailyrecords.load_stock_last_days(s.stock_no,6)
        cc = ''
        for r in r3:
            t = "9" if r.raise_drop > 0 else "6"
            cc = t + cc
        if cc:
            update(s.pk_id,cc)
            update_daily(s.stock_no,s.trade_date,cc)
        


if __name__ == "__main__":
    run()