    #!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import math
import da
import re
import datetime
from decimal import *
import config
from config import const_root_local,init_log,dbr,dbw
import comm
import util
from util import browser

loger = init_log("suggest")

#http://www.cnblogs.com/kingwolfofsky/archive/2011/08/14/2138081.html

def get_current_hhmm():
    return int(datetime.datetime.now().strftime('%Y%m%d%H%M')[8:])

def load_high_stocks():
    #'high_date_90=trade_date and high_date_188=trade_date and close=high and open<>close';
    results = dbr.select('stock_base_infos',where="high_date_188=trade_date and market_code<>'sb'")
    return list(results)

def get_last_count(field_name):
    sql="SELECT count(*) as count FROM `stock_base_infos` where  %s=trade_date;" % (field_name)
    return list(dbr.query(sql))[0].count

def get_all_count():
    d = web.storage()
    fields = ['high_date_7','high_date_30','high_date_90','high_date_188','high_date_365','low_date_7','low_date_30','low_date_90','low_date_188','low_date_365']
    for f in fields:
        d[f] = get_last_count(f)
    return d

def get_plate_cout():
    sql="SELECT market_code,count(*) as count  FROM `stock_base_infos` where high_date_188=trade_date and market_code<>'sb' group by market_code order by count(*) desc;"
    return list(dbr.query(sql))

def get_local_file_name():
    strHM = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    strHM = strHM[0:-1] #10分钟一次
    return '%s/dailym/%s.txt' %(const_root_local,strHM)

def get_suggest_local_file_name():
    strHM = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    strHM = strHM[0:-1] 
    return '%s/suggest/%s.htm' %(const_root_local,strHM)

buy_stocknos = ['600879','601766','000921']

def run():
    lfile = get_local_file_name()
    loger.info(lfile)

    #generate url
    observe_stocks = load_high_stocks()

    last_stocks_rate_range_stocknos =  [r.stock_no for r in observe_stocks if r.prate>0.03 and r.prate<0.07]

    stocks = observe_stocks + da.stockbaseinfos.load_by_stocknos(buy_stocknos) #load_by_stocknos 额外指定已购买的
    params = ['%s%s'%(s.pinyin2,s.stock_no)  for s in stocks]
    params = list(set(params))
    url = config.const_base_url + ','.join(params)

    browser.downad_and_save(url,lfile)
    rows = comm.parse_daily_data(lfile)
    for r in rows:
        r.should_sell = 'sell' if float(r.close_price) < float(r.last_close)*0.98 else '...'
        r.last = [s for s in stocks if s.stock_no == r.stock_no][0]
        r.last_in_range = r.stock_no in last_stocks_rate_range_stocknos

    content = send_reports_withT(rows)
    with open(get_suggest_local_file_name(),'w') as f:
        f.write(content)
        f.close()
    #send email
    subject='stock_%s' % (datetime.datetime.now().strftime('%m%d_%H%M')[0:-1])
    util.emailsmtp.sendmail(subject,content,['462042991@qq.com']) #,'5632646@qq.com'


def send_reports_withT(rows):
    i=0
    rows = sorted(rows, cmp=lambda x,y : cmp(y.last.volumn, x.last.volumn))
    for r in rows:
        r.last_volume_index = i
        i = i + 1

    i=0
    rows = sorted(rows, cmp=lambda x,y : cmp(y.volume, x.volume))
    for r in rows:
        r.today_volume_index = i
        i = i + 1

    i=0
    rows = sorted(rows, cmp=lambda x,y : cmp(y.raise_drop_rate, x.raise_drop_rate))
    for r in rows:
        r.raise_drop_index = i
        i = i + 1
    if len(rows)==0:
        return ""
    data = web.storage(stocks=rows,
        total_count = len(rows),
        last_close_up_count = len( [r for r in rows if r.last.close > r.last.open]),
        today_current_up_count = len( [r for r in rows if r.close_price > r.open_price]),
        today_new_high_count = len( [r for r in rows if r.is_new_high]) ,
        sell_count = len( [r for r in rows if r.raise_drop_rate< -0.019]) ,
        title = "%s %s" % (rows[0].date,rows[0].time),
        buy_stocks = buy_stocknos,
        count = get_all_count(),
        plate_count = get_plate_cout()
        )

    render_suggest = web.template.frender('templates/suggest.html')
    return str(render_suggest(data))

def run_release():
    while True:
        if not comm.is_trade_time() :
            print "it's not tradding time !"
            time.sleep(1200)
            continue
        run()
        time.sleep(600)

import time
if __name__ == '__main__':    
    run_release()
    #run()


