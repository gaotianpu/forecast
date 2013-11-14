#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import urllib
import datetime
import os
import BeautifulSoup
from config import dbr,dbw,const_root_local,init_log
import browser
import da

const_root_url = 'http://app.finance.ifeng.com/list/stock.php?'
const_market_codes = 'ha,sa,hb,sb,zxb,cyb,zs'

loger = init_log("stock_base_infos")

def get_url(params):
    return const_root_url + '&'.join(["%s=%s" % (k,v) for k,v in params.items()])

def get_local_file_name(params):
    today_path = '%s/base_%s' % (const_root_local,params['date'].strftime('%Y%m%d'))
    if not os.path.exists(today_path):
        os.mkdir(today_path)
    return '%s/%s_%s.html' % (today_path,params['t'],params['p'])

    fsegs = '_'.join(["%s-%s" % (k,v) for k,v in params.items()])
    local_file = params['date'].strftime('%Y%m%d') + '_' + fsegs + '.html'
    lfile = '%s/%s' %(const_root_local,local_file)
    return lfile

def download(params):
    print get_url(params)
    lfile = get_local_file_name(params)
    if not os.path.exists(lfile):
        url = get_url(params)
        print url
        loger.info(url)
        browser.downad_and_save(url,lfile)
        #req = urllib.urlretrieve(url,lfile)  #try..catch ... logging?
    print lfile
    return lfile

def parse_html(lfile):
    soup = BeautifulSoup.BeautifulSoup(open(lfile))
    tables =  soup.findAll('table')

    if len(tables)<1:
        return False

    result = []
    allrows = tables[0].findAll('tr')
    for row in allrows:
        result.append([])
        allcols = row.findAll('td')
        for col in allcols:
          thestrings = [unicode(s) for s in col.findAll(text=True)]
          thetext = ''.join(thestrings)
          result[-1].append(thetext)

    return [r for r in result if len(r)>4]


####


def import_to_db(params,results):
    stock_nos = load_all_stock_nos()
    l = []
    for r in results:
        if r[0] not in stock_nos:
            row = {'market_code':params['t'],'stock_no':r[0],'stock_name':r[1],'create_date':datetime.datetime.now(),'last_update':datetime.datetime.now()}
            print row
            l.append(row)


    dbw.supports_multiple_insert = True
    dbw.multiple_insert('stock_base_infos',l)

def load_all_stock_nos():
    results = dbr.select('stock_base_infos',what='stock_no')
    l = [r.stock_no for r in results]
    return l

##########

def download_all_stocks(str_date,func,loger):
    market_code_li = const_market_codes.split(',')
    for t in market_code_li:
        for p in range(1,1000):
            params = {'t':t,'p':p,'f':'symbol','o':'asc','date':str_date}
            fname = download(params)
            results = parse_html(fname)
            if not results:
                print t + " finished " + str(p)
                break
            func(params,results)

def load_from_txt():
    txt_stocks = []
    with open('stocks.txt','r') as f:
        txt_stocks = f.read().split(',')
        f.close()

    rows = da.stockbaseinfos.load_all_stocks()
    db_stocks = [r.stock_no for r in rows]
    #print set(db_stocks) ^ set(txt_stocks)
    myrows = list( set(txt_stocks) - set(db_stocks))
    l=[]
    #print set([r[:1] for r in myrows])
    #return [0,2,3,6]

    for r in myrows:
        #print r[:1],r[:1] in ['0','2','3']
        if r.startswith('6'):
            market_code_yahoo = 'ss'
            pinyin2 = 'sh'
        elif r[:1] in ['0','2','3']:
            market_code_yahoo = 'sz'
            pinyin2 = 'sz'
        else:
            #1:基金,5:退市
            continue
        l.append({'market_code_yahoo':market_code_yahoo,'stock_no':r,'pinyin2':pinyin2,'create_date':datetime.datetime.now(),'days':0})
        print market_code_yahoo,pinyin2,r
    #print l
    da.stockbaseinfos.import_daily_records('stock_base_infos',l)



if __name__ == '__main__':
    #download_all_stocks(datetime.datetime.now(),import_to_db,loger)
    load_from_txt()
    #print parse_html('/Users/gaotianpu/Documents/stocks/base_20131008/ha_20.html')


