#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
from datetime import datetime,date,timedelta

def _________________load_all_dates():
    #查询速度太慢
    return dbr.select('stock_daily_records',what="date,count(pk_id) as count", where="volume>0",
     group="date",order="date desc")

def load_trade_dates_range():
    r = dbr.select('stock_daily_records',
        what='max(date) as max_date,min(date) as min_date, (TO_DAYS(max(date)) - TO_DAYS(min(date))) as days ')
    return r[0]

def load_stocks_date(date):
    li = list(dbr.select('stock_daily_records',what="stock_no,raise_drop,volume_updown_rate",
        where="date=$date and volume>0",order='stock_no',vars=locals()))
    print li
    total_count = len(li)
    if total_count==0:
        return False
    print total_count
    price_up_count = len([stock for stock in li if stock.raise_drop>0])
    volumn_up_count = len([stock for stock in li if stock.volume_updown_rate>0])
    price_up_percent = float(price_up_count) / float(total_count) * 100
    volumn_up_percent = float(volumn_up_count) / float(total_count) * 100
    print price_up_count,volumn_up_count,price_up_percent,volumn_up_percent
    return web.storage(date=date,total_count=total_count,price_up_count=price_up_count,volumn_up_count=volumn_up_count,
        price_up_percent=price_up_percent,volumn_up_percent=volumn_up_percent)


def update_date_sum(date,data,plate=0):
    rows = list(dbr.select('date_sum_infos',where="date=$date and plate=$plate",vars=locals()))
    if len(rows)==0:
        dbw.insert('date_sum_infos',date=date,plate=plate,create_date=web.SQLLiteral("NOW()"),last_update=web.SQLLiteral("NOW()"))
    dbw.update('date_sum_infos',
        total_count = data.total_count,
        price_up_count = data.price_up_count,
        volumn_up_count = data.volumn_up_count,
        price_up_percent = data.price_up_percent,
        volumn_up_percent = data.volumn_up_percent,
        where="date=$date and plate=$plate",vars=locals())

def load_dates(plate=0):
    return [r.date for r in dbr.select('date_sum_infos',what="distinct date",where="plate=$plate",vars=locals())]

def insert_dates():
    pass

def _______________________________update_date_sum_v2(plate=0):
    #速度太慢，淘汰
    sql='''update date_sum_infos a,
    (SELECT date,'%s' as plate, count(pk_id) as count FROM stock_daily_records WHERE raise_drop is not null and raise_drop>0 GROUP BY date) as b
    set a.price_up_count=b.count
    where a.date=b.date and a.plate=b.plate;''' % (plate)
    dbw.query(sql)

    sql='''update date_sum_infos a,
    (SELECT date,'%s' as plate, count(pk_id) as count FROM stock_daily_records WHERE volume_updown_rate is not null and volume_updown_rate>0 GROUP BY date) as b
    set a.volumn_up_count=b.count
    where a.date=b.date and a.plate=b.plate;''' % (plate)
    dbw.query(sql)

    sql='''update date_sum_infos set price_up_percent = price_up_count/total_count,volumn_up_percent=volumn_up_count/total_count;'''
    dbw.query(sql)


def ____________________________run():
    dates = load_all_dates()
    for d in dates:
        data = load_stocks_date(d.date)
        if d.count != data.total_count:
            raise Exception('no stocks')
        print d.date, ' '.join(['%s=%s' % (k,v) for k,v in data.items()])
        update_date_sum(d.date,data)

def run_1():
    d = load_trade_dates_range()
    for i in range(0,d.days+1): #
        cday = d.max_date - timedelta(i)
        if cday.weekday()>4:
            print '%s is weekend' % (cday)
            continue
        data = load_stocks_date(cday)
        if data:
            update_date_sum(cday,data)

if __name__ == "__main__":
    run_1()
    #update_date_sum_v2()
    #run()
