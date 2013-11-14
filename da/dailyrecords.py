#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import datetime
from config import dbr,dbw,const_root_local,init_log


def update(pk_id,**kv):
    dbw.update('stock_daily_records',where='pk_id=$pk_id',vars=locals(),**kv)

def update_marketcode(date):
    dbw.query("update `stock_daily_records` a, stock_base_infos b set a.stock_market_no=b.market_code where a.date='"+ date.strftime('%Y%m%d') +"' and a.stock_no = b.stock_no")

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
    rows = dbr.query(sql)
    insert_date_sum(str_date,rows)

    sql = '''SELECT stock_market_no as stock_plate,count(*) as stock_count,
        avg(open_price) as open,avg(high_price) as high,avg(low_price) as low,avg(close_price) as close,avg(volume) as volume,avg(amount) as amount
        FROM `stock_daily_records` where date='%s' group by stock_market_no''' % (str_date)
    rows = dbr.query(sql)
    insert_date_sum(str_date,rows)


def insert_date_sum(trade_date,rows):
    for r in rows:
        dbw.insert('date_sums',trade_date=trade_date,stock_plate=r.trade_date,
        stock_count=r.stock_count,avg_open=r.avg_open,avg_close=r.avg_close,
        avg_high=r.avg_high,avg_low=r.avg_low,avg_volume=r.avg_volume,
        avg_amount=r.avg_amount,create_date=datetime.datetime.now())
