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
    price_raise_sum = sum([r.raise_drop for r in li if r.raise_drop>0]) / total_count * 100 
    price_up_count = len([stock for stock in li if stock.raise_drop>0])
    volumn_up_count = len([stock for stock in li if stock.volume_updown_rate>0])
    price_up_percent = float(price_up_count) / float(total_count) * 100
    volumn_up_percent = float(volumn_up_count) / float(total_count) * 100
    print price_up_count,volumn_up_count,price_up_percent,volumn_up_percent
    return web.storage(date=date,total_count=total_count,price_up_count=price_up_count,volumn_up_count=volumn_up_count,
        price_up_percent=price_up_percent,volumn_up_percent=volumn_up_percent,price_raise_sum=price_raise_sum)


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
      #  price_raise_sum = data.price_raise_sum,
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

def tmp():
    fields = ['open_price','high_price','low_price','close_price','volume','raise_drop','raise_drop_rate','volume_updown','volume_updown_rate']
    for f in fields:
        dbw.query('ALTER TABLE date_sum_infos ADD avg_%s decimal(8,2);' % (f) )
    return

def run_avg_daily(startm,endm):
    fields = ['open_price','high_price','low_price','close_price','volume','raise_drop','raise_drop_rate','volume_updown','volume_updown_rate']

    str_what = ','.join(['avg(%s) as avg_%s' %(field,field)  for field in fields])
    sql = "SELECT date,%s FROM `stock_daily_records` where date>='%s' and date<'%s' and volume>0 GROUP BY date order by date desc;" % (str_what,startm,endm)
    l = list(dbr.query(sql))
    for i in l:
        dbw.query("update date_sum_infos set %s where date='%s'" % (','.join(['%s=%s'%(k,v) for k,v in i.items() if k!='date']),i.date))

        #print ','.join(['%s=%s'%(k,v) for k,v in i.items() if k!='date'])
        #print i.key,i.value
        #str_fields = ','.join(['avg_%s=avg_%s' %(r.key,field)  for r in l])
    #

def run_moths():
    d = load_trade_dates_range()
    for i in range(0,d.days+1,30): #
        begin = d.max_date - timedelta(i)
        end = d.max_date - timedelta(i-30)
        run_avg_daily(begin.strftime('%Y-%m-01'),end.strftime('%Y-%m-01'))



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
    run_moths()
    #run_1()
    #update_date_sum_v2()
    #run()
