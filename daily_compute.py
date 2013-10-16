#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
import datetime

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

def update_v2(l):
    dbw.delete('stock_daily_records_tmp',where="pk_id>0",vars=locals())
    dbw.supports_multiple_insert = True
    dbw.multiple_insert('stock_daily_records_tmp',l)
    dbw.query('''update stock_daily_records a,stock_daily_records_tmp t set
        a.raise_drop=t.raise_drop,
        a.raise_drop_rate=t.raise_drop_rate,
        a.volume_updown=t.volume_updown,
        a.volume_updown_rate=t.volume_updown_rate,
        a.last_update = t.last_update
        where a.pk_id=t.pk_id''')


def compute_rate(stock_no):
    l = []
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
        volume_updown_rate = float(volume_updown) / pre_date_stock.volume * 100

        l.append(web.storage(pk_id=stock.pk_id,raise_drop=raise_drop,raise_drop_rate=raise_drop_rate,
            volume_updown=volume_updown,volume_updown_rate=volume_updown_rate,
            last_update=datetime.datetime.now()))
    try:
        update_v2(l)
    except Exception,e:
        loger.error(stock_no + " " + str(e) )


def run():
    stocknos = get_all_stocknos()
    for stock in stocknos:
        try:
            compute_rate(stock.stock_no)
        except Exception,e:
            print e
            loger.error(stock.stock_no + " exception " + str(e))


if __name__ == "__main__":
    run()

'''
CREATE TABLE `stock_daily_records_tmp` (
  `pk_id` int(11) unsigned NOT NULL,
  `raise_drop` decimal(8,2) DEFAULT NULL,
  `raise_drop_rate` decimal(7,3) DEFAULT NULL,
  `volume_updown` bigint(11) DEFAULT NULL,
  `volume_updown_rate` decimal(11,3) DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8;
'''

