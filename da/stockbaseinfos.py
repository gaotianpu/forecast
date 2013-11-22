#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import datetime
from config import dbr,dbw,const_root_local,init_log

def load_all_stocks():
    return list(dbr.select('stock_base_infos',
        what='pk_id,stock_no,market_code,market_code_yahoo,pinyin2',
        where="days<>0",
        #where="market_code_yahoo in ('ss','sz')",
        #offset=0,limit=1,
        order="market_code,stock_no"))

def update(stockno,stockname,openp,close,high,low,volumn,amount,trade_day):
    #
    dbw.update('stock_base_infos',
        stock_name=stockname,
        open=openp,close=close,high=high,low=low,volumn=volumn,amount=amount,trade_date=trade_day,
        last_update=web.SQLLiteral('NOW()'),
        where="stock_no=$stockno",vars=locals())

def update_high_low(stock_no,rows):
    rows['high_low_update_date'] = datetime.datetime.now()
    sql = 'update stock_base_infos set %s where stock_no=%s' %(','.join(["%s='%s'" % (k,v) for k,v in rows.items()]),stock_no)
    dbw.query( sql )


def import_daily_records(table,rows):
    dbw.supports_multiple_insert = True
    dbw.multiple_insert(table,rows)

if __name__ == '__main__':
     load_all_stocks()

