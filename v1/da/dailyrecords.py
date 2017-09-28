#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import datetime
from config import dbr,dbw,const_root_local,init_log


def update(pk_id,**kv):
    dbw.update('stock_daily_records',where='pk_id=$pk_id',vars=locals(),**kv)

def update_marketcode(date):
    dbw.query("update `stock_daily_records` a, stock_base_infos b set a.stock_market_no=b.market_code where a.date='"+ date.strftime('%Y-%m-%d') +"' and a.stock_no = b.stock_no")

def load_by_date(date):
    return dbr.select('stock_daily_records',what='pk_id,stock_no',where='date=$date',vars=locals())

def load_pkids(date):
    pkids = {}
    rows = load_by_date(date)
    for r in rows:
        pkids[r.stock_no] = r.pk_id
    return pkids

def load_by_stockno(stock_no):
    return list(dbr.select('stock_daily_records',where="stock_no=$stock_no and volume>0", order="date desc",vars=locals()))

def import_date_sums(str_date):
    sql = '''SELECT 'all' as stock_plate,count(*) as stock_count,
        avg(open_price) as open,avg(high_price) as high,avg(low_price) as low,avg(close_price) as close,avg(volume) as volume,avg(amount) as amount
        FROM `stock_daily_records` where date='%s' ''' % (str_date)
    #rows = dbr.query(sql)
    #insert_date_sum(str_date,rows)

    sql = '''SELECT stock_market_no as stock_plate,count(*) as stock_count,
        avg(open_price) as open,avg(high_price) as high,avg(low_price) as low,avg(close_price) as close,avg(volume) as volume,avg(amount) as amount
        FROM `stock_daily_records` where date='%s' and stock_market_no is not null group by stock_market_no''' % (str_date)
    rows = dbr.query(sql)
    insert_date_sum(str_date,rows)

    sql = '''SELECT stock_market_no as stock_plate,count(*) as stock_count
        FROM `stock_daily_records` where date='%s' and stock_market_no is not null and raise_drop>0 group by stock_market_no  ''' % (str_date)
    rows = dbr.query(sql)
    for r in rows:
        stock_plate = r.stock_plate
        dbw.update('date_sums',price_up_count=r.stock_count, where="trade_date=$str_date and stock_plate=$stock_plate",vars=locals())
    dbw.query("update date_sums set price_up_percent=price_up_count/stock_count where trade_date='%s'" % (str_date) )


def insert_date_sum(trade_date,rows):
    dbw.delete("date_sums",where="trade_date=$trade_date",vars=locals())
    for r in rows:
        dbw.insert('date_sums',trade_date=trade_date,stock_plate=r.stock_plate,
        stock_count=r.stock_count,avg_open=r.open,avg_close=r.close,
        avg_high=r.high,avg_low=r.low,avg_volume=r.volume,
        avg_amount=r.amount,create_date=datetime.datetime.now())


def load_max_min(stock_no,days):
    result = {}

    high = list(dbr.select('stock_daily_records',
        what="date,high_price",
        where="stock_no=$stock_no and volume<>0 and TO_DAYS(NOW())-TO_DAYS(date) < $days",
        offset=0,limit=1,
        order="high_price desc",
        vars=locals()))

    if high:
        result['high_date_%s'%(days)]=high[0].date
        result['high_price_%s'%(days)]=high[0].high_price


    low = list(dbr.select('stock_daily_records',
        what="date,low_price",
        where="stock_no=$stock_no and volume<>0 and TO_DAYS(NOW())-TO_DAYS(date) < $days",
        offset=0,limit=1,
        order="low_price asc",
        vars=locals()))

    if low:
        result['low_date_%s'%(days)]=low[0].date
        result['low_price_%s'%(days)]=low[0].low_price

    high_v = list(dbr.select('stock_daily_records',
        what="date,volume",
        where="stock_no=$stock_no and volume<>0 and TO_DAYS(NOW())-TO_DAYS(date) < $days",
        offset=0,limit=1,
        order="high_price desc",
        vars=locals()))[0]

    low_v = list(dbr.select('stock_daily_records',
        what="date,volume",
        where="stock_no=$stock_no and volume<>0 and TO_DAYS(NOW())-TO_DAYS(date) < $days",
        offset=0,limit=1,
        order="low_price asc",
        vars=locals()))[0]

    return result

def load_all_last_5():
    #加载过去5天内股票
    #SELECT * FROM `stock_daily_records` WHERE TO_DAYS(NOW())-TO_DAYS(date) < 8 and volume<>0 order by stock_no,date desc
    results = dbr.select('stock_daily_records',
        where="TO_DAYS(NOW())-TO_DAYS(date) < 8 and volume<>0", #考虑到排除周末情况？
        order="date desc",vars=locals())
    return list(results)

def load_stock_last_days(stock_no,days):
    results = dbr.select('stock_daily_records',
        where="stock_no=$stock_no and volume<>0", #考虑到排除周末情况？
        order="date desc",limit=days,vars=locals())
    return list(results)

def remove_daily_records(date):
    results = dbr.select('stock_daily_records',where="date=$date",vars=locals())
    fields =  ['date','stock_no','open_price','high_price','low_price','close_price','create_date','last_update', 'volume','amount','adj_close','raise_drop','raise_drop_rate','is_traday','volume_updown','volume_updown_rate']
    for r in results:
        str_field_value_list = ','.join(["%s='%s'" % (k,v)  for k,v in r.items()  if k in fields and v is not None])         
        dbw.query('replace into forecast_backup.z_%s set %s' % (r.stock_no,str_field_value_list))


def import_history_rows(stock_no,rows):
    fields =  ['date', 'open_price','high_price','low_price','close_price', 'volume','amount','adj_close']
    for r in rows:
        str_field_value_list = ','.join(["%s='%s'" % (k,v)  for k,v in r.items()  if k in fields and v is not None])         
        dbw.query('replace into forecast_backup.z_%s set %s' % (stock_no,str_field_value_list))