#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
import browser
import datetime
import os
import csv

#doc:http://www.bizeway.net/read.php?317 
#http://table.finance.yahoo.com/table.csv?s=000001.sz

loger = init_log("history_daily")
const_root_url = "http://table.finance.yahoo.com/table.csv?" 

def get_url(params):
    return '%ss=%s' % (const_root_url,params['s'])

def get_local_file_name(params): 
    return '%s/dailyh/%s.csv' %(const_root_local,params['s'])
    #return lfile

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
    return list(dbr.select('stock_base_infos', 
        what='stock_no,market_code,market_code_yahoo',
        where="market_code_yahoo in ('ss','sz')",
        order="market_code,stock_no"))

def load_stock_dates(stock_no):
    rows = dbr.select('stock_daily_records',what='date',where="stock_no=$stock_no", vars=locals())
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
        scode = '%s.%s' % (s.stock_no,s.market_code_yahoo)
        #params={'s':scode}
        params={'s':scode,'a':'00','b':'01','c':2013,'d':'9','e':'01','f':'2013','g':'d'}  
        lfile = get_local_file_name(params)
        url = get_url(params)  
        try:
            if not os.path.exists(lfile):
                print url        
                loger.info("downloading " + url)  
                browser.downad_and_save(url,lfile)
            data = parse_data(lfile)
            import_stock_daily_data(s.market_code,s.stock_no,data)
        except Except,e:
            loger.err(" except "+ e + url)
            

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
    download_all(load_all_stocks()) 
    #stocks = load_failed_stock()
    #download_all(stocks) 
    
    #download(params)
    #test_one_stock()
    
    


