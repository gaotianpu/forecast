#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import urllib 
import urllib2
import random
import datetime
import os
import csv
from config import dbr,dbw,const_root_local,init_log
import da
import browser

#doc:http://blog.t41.cn/index.php/archives/254 
#http://table.finance.yahoo.com/table.csv?s=000001.sz



const_root_url = "http://ichart.yahoo.com/table.csv?"
params={'s':'600000.SS','a':'00','b':'01','c':2013,'d':'09','e':'01','f':'2013','g':'d'}
mcodes = {'sa':'sz','sb':'sz','ha':'ss','hb':'ss','zs':'','ss':'ss','sz':'sz'}

def get_url(params):
    return '%ss=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=%s' % (const_root_url,params['s'],params['a'],params['b'],params['c'],params['d'],params['e'],params['f'],params['g'])
    return const_root_url + '&'.join(["%s=%s" % (k,v) for k,v in params.items()])

def get_local_file_name(params):    
    local_file = '%s_%s%s%s_%s%s%s_%s.csv' % (params['s'],params['c'],params['b'],params['a'],params['f'],params['e'],params['d'],params['g'])
    lfile = '%s/dailyh/%s' %(const_root_local,local_file)
    return lfile

def download(params):
    lfile = get_local_file_name(params)
    if not os.path.exists(lfile):
        url = get_url(params)
        print url
        try:
            browser.downad_and_save(url,lfile)
        except Exception,ex:
            print "urlretrieve except,%s,%s" % (url,str(ex))
            return False
            
    print lfile
    return lfile


def parse_data(lfile):
    l=[]
    with open(lfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for date,openp,highp,lowp,closep,volume,adjclose in reader:
            if date == 'Date':
                continue
            l.append({'date':date,'open_price':openp,'high_price':highp,
                'low_price':lowp,'close_price':closep,'volume':volume,'adj_close':adjclose}) 
    return l

##database operations
def load_all_stocks():
    return list(dbr.select('stock_base_infos',what='stock_no,market_code'))

def load_stock_dates(stock_no):
    rows = dbr.select('stock_daily_records',what='date',where="stock_no=$stock_no",vars=locals())
    dates = [row.date.strftime('%Y-%m-%d')  for row in rows]
    return dates

    
def import_stock_daily_data(market_code,stock_no,data):
    stock_dates = load_stock_dates(stock_no)   

    l=[]
    for row in data:
        if row['date'] in stock_dates:
            #print  '%s.%s %s exists in db' % (market_code,stock_no,row['date'])
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

###
def download_all(stocks):    
    for s in stocks:
        if not mcodes[s.market_code]:
            print 'sz:'+s.stock_no
            continue 
        scode = '%s.%s' % (s.stock_no,mcodes[s.market_code])
        params={'s':scode,'a':'00','b':'01','c':2013,'d':'9','e':'01','f':'2013','g':'d'}
        lfile = download(params)
        break
        if lfile:
            data = parse_data(lfile)
            import_stock_daily_data(s.market_code,s.stock_no,data)

def load_failed_stock():
    #cat  github/forecast/log2.txt  | grep 'except' | awk -F '[=&]' '{print $4}' > github/forecast/fail_stocks.txt
    l = []
    with open('fail_stocks.txt') as f:
        reader = csv.reader(f, delimiter='.')
        for stock_no,market_code in reader:            
            l.append(web.storage(market_code=market_code,stock_no=stock_no))
    return l           
        
def test_one_stock():
    lfile = download(params)
    data = parse_data(lfile)
    import_stock_daily_data('sa','600000',data)

if __name__ == '__main__':  
    #download_all(load_all_stocks()) 
    stocks = load_failed_stock()
    download_all(stocks) 
    
    #download(params)
    #test_one_stock()
    
    


