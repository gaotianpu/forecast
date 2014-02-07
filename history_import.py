#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
from util import browser
import datetime
import os
import csv
import da,comm

#doc:http://www.bizeway.net/read.php?317
#http://table.finance.yahoo.com/table.csv?s=000001.sz

loger = init_log("stock_history_daily")
const_root_url = "http://table.finance.yahoo.com/table.csv?"

def load_stock_dates(stock_no):
    rows = dbr.select('stock_daily_records',what='date',where="stock_no=$stock_no", vars=locals())
    dates = [row.date.strftime('%Y-%m-%d')  for row in rows]
    return dates


def import_stock_daily_data(market_code,stock_no,data):
    stock_dates = load_stock_dates(stock_no)
    max_date = max(stock_dates) if stock_dates else '1900-01-01'
    l=[]
    for row in data:
        #if row['date'] <= max_date: break
        if row['date'] in stock_dates:
            continue
        row['stock_market_no'] = market_code
        row['stock_no'] = stock_no
        row['create_date'] = datetime.datetime.now()
        row['last_update'] = datetime.datetime.now()
        l.append(row)

    print '%s.%s csv len is %s' %(market_code,stock_no,len(data))
    print '%s.%s insert len is %s' %(market_code,stock_no,len(l))

    dbw.supports_multiple_insert = True
    dbw.multiple_insert('stock_daily_records',l)

def import_into_db(stock,rows):
    pass


def download_and_parse_data(stock):
    scode = '%s.%s' % (stock.stock_no,stock.market_code_yahoo)
    url = '%ss=%s' % (const_root_url,scode)
    lfile = '%s/dailyh/%s.csv' %(const_root_local,scode)
    try:
        if not os.path.exists(lfile):
            print url
            loger.info("downloading " + url)
            browser.downad_and_save(url,lfile)
        rows = comm.parse_history_data(lfile)
        return rows
    except Exception,e:
        loger.error(url + " " + str(e) )
    return False


import time
def run():
    stocks = da.stockbaseinfos.load_all_stocks()
    for s in stocks:
        if int(s.stock_no) > 300000 : continue
        rows = download_and_parse_data(s)
        if not rows:
            time.sleep(30)
            continue        
        trade_dates = da.stockdaily.load_dates(s.stock_no)
        db_dates = set([r.trade_date.strftime('%Y-%m-%d') for r in trade_dates])
        file_dates = set([r.date for r in rows])
        tmp = file_dates - db_dates
        for r in rows:
            if r.date in tmp:
                da.stockdaily_cud.insert(r.date,s.stock_no,r.open_price,r.close_price,r.high_price,r.low_price,r.volume)
            else:
                pass #?update
           
        print s.stock_no,'end'       

if __name__ == '__main__':
    run()