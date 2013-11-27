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


def run():
    stocks = da.stockbaseinfos.load_all_stocks()
    for s in stocks:
        rows = download_and_parse_data(s)
        import_into_db(s,rows)


if __name__ == '__main__':
    run()
    #print load_all_stocks()
    #download_all(da.stockbaseinfos.load_all_stocks())

    #stock_dates = load_stock_dates('300001')
    #max_date = max(stock_dates)
    #print max_date
    #print '2012-01-01' > max_date
    #print '2014-01-01' > max_date


    #load_all_stocks()


    #stocks = load_failed_stock()
    #download_all(stocks)

    #download(params)
    #test_one_stock()




