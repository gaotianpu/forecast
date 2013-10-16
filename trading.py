#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
from datetime import datetime,date,timedelta

import random

loger = init_log("trading")

def load_dates_stock(stock_no,buy_date,hold_days):    
    r = dbr.select('stock_daily_records',
        where="stock_no=$stock_no and volume>0 and date>=$buy_date", offset=0,limit=hold_days+1,order="date asc", vars=locals())
    return list(r)

def buy_and_sell(strategy_id,strategy_batch_no,stock_no,buy_date,hold_days=1,buy_price='open_price',sell_price='open_price',trade_hands=1):
    stocks = load_dates_stock(stock_no,buy_date,hold_days)  
    if len(stocks)< hold_days + 1: 
        raise Exception('no sell date stock info')   
    buy_stock = stocks[0]
    sell_stock = stocks[-1]    

    earnings = ( sell_stock[sell_price] - buy_stock[buy_price] )*  trade_hands * 100 
    earnings_rate = ( sell_stock[sell_price] - buy_stock[buy_price] )/ buy_stock[buy_price] * 100 

    dbw.insert('trading_records',
        strategy_id = strategy_id,
        strategy_batch_no = strategy_batch_no,
        buy_or_sell = 0,
        stock_no = buy_stock.stock_no,
        date = buy_stock.date,
        open_or_close = buy_price,
        price = buy_stock[buy_price],
        hands = trade_hands,
        input_output = 0 - buy_stock[buy_price] * trade_hands  * 100 ,
        earnings=earnings,earn_rate=earnings_rate,
        create_date=web.SQLLiteral('now()'))

    dbw.insert('trading_records',
        strategy_id = strategy_id,
        strategy_batch_no = strategy_batch_no,
        stock_no = sell_stock.stock_no,
        buy_or_sell = 1,
        date = sell_stock.date,
        open_or_close = sell_price,
        price = sell_stock[sell_price],
        hands = trade_hands,
        input_output =  sell_stock[sell_price] * trade_hands  * 100 ,
        earnings = earnings, earn_rate=earnings_rate,
        create_date=web.SQLLiteral('now()'))

def run_strategy_sum(strategy_id):
    sql='''update trading_strategies s,
(select strategy_id,max(earn_rate) as max_earn_rate,
    min(earn_rate) as min_earn_rate, 
    sum(earnings)/sum(input_output)*100 as avg_earn_rate,
    count(*) as trade_count from `trading_records` where strategy_id=%s and buy_or_sell=1) as ss
set s.max_earn_rate=ss.max_earn_rate,
s.min_earn_rate = ss.min_earn_rate,
s.avg_earn_rate = ss.avg_earn_rate,
s.trade_count = ss.trade_count,
s.last_update = now()
where s.pk_id=ss.strategy_id;
    ''' % (strategy_id)
    dbw.query(sql)

##################################

def run_strategy_1():
    strategy_id = 1
    dates = [r.date for r in  dbr.select('stock_daily_records',what="distinct date",where="volume>0")]
    stock_nos = [r.stock_no for r in  dbr.select('stock_daily_records',what="distinct stock_no",where="volume>0")]
    for i in range(0,1000):
        stock_no = random.choice(stock_nos)
        date = random.choice(dates)
        try:
            buy_and_sell(strategy_id,i,stock_no,date)
        except Exception,e:
            print e
            loger.error("stock_no=%s&date=%s&error=%s" %(stock_no,date,e)) 
    run_strategy_sum(strategy_id)    

if __name__ == "__main__":
    run_strategy_1()
    #run_strategy_sum(1)
    #buy_and_sell(1,1,600000,'2013-09-23',1)
    #print random.randrange(1000)
    #run(filter_stocks_func,strategy,date)


