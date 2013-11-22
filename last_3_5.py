#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
import da

def update(stock_no,result):
    pass

def compute_trend(rows):
    rows = sorted(rows, cmp=lambda x,y : cmp(x.close_price, y.close_price))

    i=1
    for r in rows:
        r.index = i
        i = i + 1

    t=''
    rows = sorted(rows, cmp=lambda x,y : cmp(x.date, y.date))
    for r in rows:
        t = t + str(r.index)

    return int(t)


def compute_5_3(stock_trade_records_5):
    days_count = len(stock_trade_records_5)

    day_0 = stock_trade_records_5[0]
    day_5 = stock_trade_records_5[-1]
    day_3 = stock_trade_records_5[2] if days_count>3 else stock_trade_records_5[-1]

    #涨幅
    day_3_price_rate = (day_0.close_price - day_3.open_price)/day_3.open_price
    day_5_price_rate = (day_0.close_price - day_5.open_price)/day_5.open_price

    #趋势线
    trend_3 = compute_trend(stock_trade_records_5[0:3] if days_count>3 else stock_trade_records_5)
    trend_5 = compute_trend(stock_trade_records_5)

    #print trend_3,day_3_price_rate,trend_5,day_5_price_rate
    return web.storage(days_count=days_count,trend_5=trend_5,trend_3=trend_3,
        day_3_price_rate=day_3_price_rate,day_5_price_rate=day_5_price_rate)

def run():
    trade_records_5 = da.dailyrecords.load_all_last_5()

    stocks = [web.storage(stock_no='000001')] #da.stockbaseinfos.load_all_stocks()
    for s in stocks:
        stock_trade_records_5 = [r for r in trade_records_5 if r.stock_no==s.stock_no]
        if not stock_trade_records_5:
            continue
        result = compute_5_3(stock_trade_records_5)
        print result
        update(s.stock_no,result)


if __name__ == "__main__":
    run()
