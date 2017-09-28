#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
from config import dbr,dbw,const_root_local,init_log
import datetime

loger = init_log("daily_compute")

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

def insert_trend_data(pkid,stock_no,h5,h3,l5,l3):
    dbw.query('replace into trend_daily(pkid,stock_no,date,high5,high3,low5,low3)values')

def compute_rate(stock_no):
    l = []
    stocks = da.dailyrecords.load_by_stockno(stock_no)
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

def __compute_trend(date_infos,index,days,price_type):
    sub_dates = date_infos[index : index + days]

    sub_dates.sort(lambda a,b:cmp(a[price_type],b[price_type]))
    x = 1
    for d in sub_dates:
        d.no = x
        x = x + 1

    sub_dates.sort(lambda a,b:cmp(a['date'],b['date']))

    hp = ''
    for d in sub_dates:
        hp = hp + str(d.no)
        #print days,d.date,d.high_price,d.low_price,d.open_price,d.close_price,d.no

    return hp

def compute_3or5(stock_no):
    date_infos = da.dailyrecords.load_by_stockno(stock_no)
    date_len = len(date_infos)

    rows = []
    for i in range(0,date_len):
        print i
        stock_date = date_infos[i]
        d = stock_date.date
        dh5 = __compute_trend(date_infos,i,5,'high_price')
        dh3 = __compute_trend(date_infos,i,3,'high_price')

        dl5 = __compute_trend(date_infos,i,5,'low_price')
        dl3 = __compute_trend(date_infos,i,3,'low_price')

        #未来n天内，收盘价 与 明天开盘价对比
        prates = {}
        tommorrow_open_price = date_infos[i-1].open_price
        for day in range(2,6):
            prates[day] = None
            if i < day : continue
            prates[day] = (date_infos[i-day].close_price - tommorrow_open_price) / tommorrow_open_price

        if i > 6:
           p = date_infos[i-6].close_price - date_infos[i-1].open_price
           prate = p/date_infos[i-1].open_price
           print stock_date.date,dh5,dh3,dl5,dl3,p,prate

        if date_len > (i+5):
            history_prate_3 = (stock_date.close_price - date_infos[i+3].close_price) / date_infos[i+3].close_price
            history_prate_5 = (stock_date.close_price - date_infos[i+5].close_price) / date_infos[i+5].close_price

        rows.append(web.storage(pk_id=stock_date.pk_id,date=stock_date.date,stock_no=stock_date.stock_no,
             high5=dh5,high3=dh3,low5=dl5,low3=dl3,tmrow_open_price=tommorrow_open_price,
             price_rate_2=prates[2],price_rate_3=prates[3],price_rate_4=prates[4],price_rate_5=prates[5],
             history_prate_3=history_prate_3,history_prate_5=history_prate_5))

        i = i + 1

    dbw.delete('trend_daily',where="stock_no=$stock_no",vars=locals())
    dbw.supports_multiple_insert = True
    dbw.multiple_insert('trend_daily',rows)


def run():
    stocknos = da.stockbaseinfos.load_all_stocks() #get_all_stocknos()
    for stock in stocknos:
        try:
            compute_rate(stock.stock_no)
        except Exception,e:
            print e
            loger.error(stock.stock_no + " exception " + str(e))

def run_3or5():
    stocknos = da.stockbaseinfos.load_all_stocks()
    for stock in stocknos:
        try:
            compute_3or5(stock.stock_no)
        except Exception,e:
            print e
            loger.error(stock.stock_no + " exception " + str(e))


if __name__ == "__main__":
    run_3or5()
    #compute_3or5(300001)
    #run()

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

