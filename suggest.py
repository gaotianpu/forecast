#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import math
import da
import re
import datetime
import browser
from decimal import *
import config
from config import const_root_local,init_log,dbr,dbw
import comm
import emailsmtp

loger = init_log("suggest")

#http://www.cnblogs.com/kingwolfofsky/archive/2011/08/14/2138081.html

def get_current_hhmm():
    return int(datetime.datetime.now().strftime('%Y%m%d%H%M')[8:])

def load_high_stocks():
    #'high_date_90=trade_date and high_date_188=trade_date and close=high and open<>close';
    results = dbr.select('stock_base_infos',where="high_date_90=trade_date and high_date_188=trade_date")
    return list(results)

def load_buy_stocks(stock_nos):
    results = dbr.select('stock_base_infos',where="stock_no in $stock_nos ",vars=locals())
    return list(results)

def get_local_file_name():
    strHM = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    strHM = strHM[0:-1] #10分钟一次
    return '%s/dailym/%s.txt' %(const_root_local,strHM)

def get_suggest_local_file_name():
    strHM = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    strHM = strHM[0:-1] #10分钟一次
    return '%s/suggest/%s.htm' %(const_root_local,strHM)


def run():
    buy_stocknos = ['600290','002290']
    if not comm.is_trade_time() :
        print "it's not tradding time !"
        #return

    lfile = get_local_file_name()
    loger.info(lfile)

    #generate url
    observe_stocks = load_high_stocks()
    stocks = observe_stocks + load_buy_stocks(buy_stocknos) #load_buy_stocks 额外指定已购买的
    params = ['%s%s'%(s.pinyin2,s.stock_no)  for s in stocks]
    params = list(set(params))
    url = config.const_base_url + ','.join(params)

    browser.downad_and_save(url,lfile)
    rows = comm.parse_daily_data(lfile)
    for r in rows:
        r.should_sell = 'sell' if float(r.close_price) < float(r.last_close)*0.98 else '...'
        r.last = [s for s in stocks if s.stock_no == r.stock_no][0]

    content = send_reports_v2(rows)
    print content
    return
    content = send_reports(rows,buy_stocknos,observe_stocks)

    #print rows
    with open(get_suggest_local_file_name(),'w') as f:
        f.write(content)
        f.close()

    #send email
    subject='stock_%s' % (datetime.datetime.now().strftime('%m%d_%H%M')[0:-1])
    emailsmtp.sendmail(subject,content,['462042991@qq.com']) #,'5632646@qq.com'


def send_reports_v2(rows):
    render_suggest = web.template.frender('templates/suggest.html')
    rows = sorted(rows, cmp=lambda x,y : cmp(y.raise_drop_rate, x.raise_drop_rate))
    data = web.storage(stocks=rows)
    return render_suggest(data)


def send_reports(rows,buy_stocknos,observe_stocks):
    #######
    content = ''
    for r in rows:
        if r.stock_no not in buy_stocknos: continue
        should_sell = 'sell' if float(r.close_price) < float(r.last_close)*0.98 else '...'
        content = content + '<a href="http://stockhtm.finance.qq.com/sstock/ggcx/%s.shtml">%s</a>,%s,%s,%s' % (r.stock_no,r.stock_no,should_sell,r.last_close,r.close_price) + '<br/>'
    #10点前的high_price是一个重要的参考点?
    tmp =[r for r in rows if r.raise_drop_rate<>-1 and r.raise_drop_rate>0.02]
    tmp = sorted(tmp, cmp=lambda x,y : cmp(y.raise_drop_rate, x.raise_drop_rate))
    content = content + '<br/>'.join(['%s,<a href="http://stockhtm.finance.qq.com/sstock/ggcx/%s.shtml">%s</a>,%s,%s,%s' % (r.is_new_high,r.stock_no,r.stock_no,r.high_price,r.close_price,r.raise_drop_rate) for r in tmp])
    content = content + '<br/>new count:%s' %(len(observe_stocks))
    content = content + '<br/>observe_stocks count:%s' %(len(tmp))
    return content


import time
if __name__ == '__main__':
    run()

    #while True:
        #run()
    #    time.sleep(600)

    #a = load_buy_stocks(['600290','000897'])
    #stocks + a
    #print datetime.datetime.now().strftime('%Y%m%d%H%M')[0:-1]

    #parse_data('D:\\gaotp\\stocks\\daily\\20131111_0.txt')


