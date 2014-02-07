#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import datetime
from config import dbr,dbw,const_root_local,init_log


def check_exist(date,stock_no):
    return list(dbr.select('stock_daily',where="trade_date=$date and stock_no=$stock_no",vars=locals()))

def insert_row(date,stock_no):
    return dbw.insert('stock_daily',trade_date=date,stock_no=stock_no,create_date = web.SQLLiteral('NOW()'),)

def insert(date,stock_no,open,close,high,low,volume):
    return dbw.insert('stock_daily',trade_date=date,stock_no=stock_no,
        open = open,
        close = close,
        high = high,
        low = low,
        volume = volume,         
        create_date = web.SQLLiteral('NOW()'),
        last_update = web.SQLLiteral('NOW()'),)

def update_last_high_low():
    trade_dates = load_trade_dates()
    today = trade_dates[0].trade_date
    last_day = trade_dates[1].trade_date   
    sql = """update stock_daily s,
        (SELECT stock_no,high_low FROM `stock_daily` where trade_date='%s' ) as last 
        set s.last_high_low = last.high_low 
        where s.trade_date='%s' and s.stock_no=last.stock_no""" % (last_day,today)
    dbw.query(sql)

def update_avg_volume_10():  
    trade_dates = load_trade_dates()

    today = trade_dates[0].trade_date
    begin_day = trade_dates[-1].trade_date
    end_day = trade_dates[1].trade_date  

    sql = """update stock_daily s,
        (SELECT stock_no,avg(volume) as avg_volume FROM `stock_daily` where trade_date BETWEEN '%s' and '%s' group by stock_no) as avg10
        set s.volume_avg_10 = avg10.avg_volume 
        where s.trade_date='%s' and s.stock_no=avg10.stock_no""" % (begin_day,end_day,today)
    dbw.query(sql)

def update_trend3(trade_date,stock_no,trend3):
    dbw.update('stock_daily',trend_3=trend3,where="trade_date=$trade_date and stock_no=$stock_no",vars=locals())

def import_rows(rows):
    date = rows[0].date 
    for r in rows:
        candle = r.candle_2
        results = check_exist(date,r.stock_no)
        pk_id = insert_row(date,r.stock_no) if not results else results[0].pk_id
        dbw.update('stock_daily',
            open=r.open_price,close=r.close_price,high=r.high_price,low=r.low_price,volume=r.volume,amount=r.amount,last_close=r.last_close,
            high_low = r.high_low, close_open = r.close_open, open_last_close = r.open_last_close, 
            jump_rate=r.jump_rate, price_rate=r.raise_drop_rate, high_rate = r.high_rate, low_rate = r.low_rate, hig_low_rate =  r.high_rate -  r.low_rate,
            range_1=candle[0],range_2=candle[1],range_3=candle[2],
            last_update = web.SQLLiteral('NOW()'),
            where='pk_id=$pk_id',vars=locals())
        
def load_trade_dates():
    sql = "SELECT DISTINCT trade_date FROM `stock_daily` ORDER BY trade_date desc limit 0,10"
    return list(dbr.query(sql))

def load_by_beginDate(date):
    return list(dbr.select('stock_daily',where="trade_date>=$date",order="stock_no", vars=locals()))


def load_for_buy(date):
    return list(dbr.select('stock_daily',
        what="stock_no",
        where="trade_date=$date and volume<>0 and trend_3=321 and range_3>5",
        order="range_3 desc",
        vars=locals()))