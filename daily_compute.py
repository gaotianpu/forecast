#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log

loger = init_log("daily_compute")

def get_all_stocknos():
    sql="select distinct stock_no from stock_daily_records order by stock_no"
    r = dbr.query(sql)
    return list(r)

def get_stock_daily_infos(stock_no):
    return list(dbr.select('stock_daily_records',where="stock_no=$stock_no and volume>0", order="date desc",vars=locals()))

def update(stock_no,date,raise_drop,raise_drop_rate,volume_updown,volume_updown_rate):
    dbw.update('stock_daily_records',
        raise_drop = raise_drop,
        raise_drop_rate = raise_drop_rate,
        volume_updown = volume_updown,
        volume_updown_rate = volume_updown_rate,
        where="stock_no=$stock_no and date=$date",vars=locals())

def compute_rate(stock_no):
    stocks = get_stock_daily_infos(stock_no)
    stocks_len = len(stocks)
    for stock in stocks:
        i = stocks.index(stock)
        if i == (stocks_len-1):
            break
        pre_date_stock =  stocks[i+1]
        raise_drop = stock.close_price - pre_date_stock.close_price
        raise_drop_rate = raise_drop / pre_date_stock.close_price * 100

        volume_updown = stock.volume - pre_date_stock.volume
        volume_updown_rate =   float(volume_updown) / pre_date_stock.volume * 100

        update(stock.stock_no,stock.date,raise_drop,raise_drop_rate,volume_updown,volume_updown_rate)

        #print i,stock.date, stock.raise_drop, stock.raise_drop_rate, stock.volume, pre_date_stock.volume,stock.volume_updown, stock.volume_updown_rate
    print stocks_len

def run():
    stocknos = get_all_stocknos()
    for stock in stocknos:
        try:
            compute_rate(stock.stock_no)
        except Exception,e:
            print e
            loger.error(stock.stock_no + " exception " + str(e))


if __name__ == "__main__":
    #compute_rate('600000')
    run()
