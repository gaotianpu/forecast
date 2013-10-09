#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from  stock_base_info import download_all_stocks
import datetime
from config import dbr,dbw,const_root_local
import re

import urllib
import os
import BeautifulSoup
import browser

def get_int(str_input):
    reg = re.compile("([\d]+)")
    m = reg.findall(str_input)
    return int(m[0]) if m else 0

###db operation
def load_records_by_date(params):
    date = params['date'].strftime('%Y-%m-%d')
    market_code = params['t']
    results = dbr.select('stock_daily_records',what='stock_no',where="date=$date and stock_market_no=$market_code",vars=locals())
    return [r.stock_no for r in  results]

###

def import_to_daily_records(params,results):
    stock_nos = load_records_by_date(params)
    l = []
    for r in results:
        if not stock_nos or r[0] not in stock_nos:
            #print get_int(r[5]), get_int(r[6])
            row = {'date':params['date'].strftime('%Y-%m-%d'),'stock_market_no':params['t'],
            'create_date':datetime.datetime.now(),'last_update':datetime.datetime.now(),
            'stock_no':r[0],
            'close_price':r[2], #?
            'raise_drop_rate':r[3],
            'raise_drop':r[4],
            'volume':get_int(r[5])*100 , #r[5], 成交量
            'amount':get_int(r[6])*10000 , #r[6], 成交额
            'open_price':r[7],
            'adj_close':r[8], #r[8], 昨收盘？？？
            'low_price':r[9],
            'high_price':r[10]
            }
            #print row
            l.append(row)

    dbw.supports_multiple_insert = True
    dbw.multiple_insert('stock_daily_records',l)

if __name__ == '__main__':
    download_all_stocks(datetime.datetime.now(),import_to_daily_records)
    #print load_records_by_date(datetime.datetime.now().strftime('%Y-%m-%d'))
