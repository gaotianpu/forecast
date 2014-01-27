#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
import comm
import util
import datetime


def run():
    dates = da.stockdaily_cud.load_trade_dates()
    today = dates[0].trade_date    
    date_3 = dates[2].trade_date      

    date_3_rows = da.stockdaily_cud.load_by_beginDate(date_3)

    stocks = da.stockbaseinfos.load_all_stocks() #[web.storage(stock_no='000001',pk_id=332)] #test
    for s in stocks:
        rows = [r for r in date_3_rows if r.stock_no==s.stock_no]
        if not rows:
            continue
        print s.stock_no,comm.get_trend(rows)
        da.stockdaily_cud.update_trend3(today,s.stock_no,comm.get_trend(rows)) 

    send_report(today)    

def send_report(today):
    #dates = da.stockdaily_cud.load_trade_dates()
    #today = dates[0].trade_date    
    stock_nos = da.stockdaily_cud.load_for_buy(today)
    l = []
    for row in stock_nos:
        code = comm.get_market_codes(row.stock_no)
        if not code['pinyin'] : continue
        l.append('<a href="http://stockhtm.finance.qq.com/sstock/ggcx/%s.shtml"><img src="http://image.sinajs.cn/newchart/daily/n/%s%s.gif" /></a>' % (row.stock_no,code['pinyin'],row.stock_no) )
    #print "".join(l)
    subject='%s trend_3=321 and range_3>5 ORDER BY range_3 desc ' % ( datetime.datetime.now().strftime('%Y-%m-%d') )
    util.emailsmtp.sendmail(subject,"".join(l),['462042991@qq.com']) 

if __name__ == "__main__":
    #send_report(False)
    run()
