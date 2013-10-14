#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log

def load_all_dates():    
    return dbr.select('stock_daily_records',what="date,count(pk_id) as count", where="raise_drop is not null",
     group="date",order="date desc")

def load_stocks_date(date):
    li = list(dbr.select('stock_daily_records',where="date=$date and raise_drop is not null",order='stock_no',vars=locals()))
    print li
    total_count = len(li)
    print total_count
    price_up_count = len([stock for stock in li if stock.raise_drop>0]) 
    volumn_up_count = len([stock for stock in li if stock.raise_drop>0]) 
    price_up_percent = price_up_count / total_count * 100
    volumn_up_percent = volumn_up_count / total_count * 100 
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

def update_date_sum_v2(plate=0):
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
    

def run():
    dates = load_all_dates()
    for d in dates:        
        data = load_stocks_date(d.date)
        if d.count != data.total_count:
            throw
        print d.date, ' '.join(['%s=%s' % (k,v) for k,v in data.items()])      
        update_date_sum(d.date,data)

if __name__ == "__main__":
    update_date_sum_v2()
    #run() 
        