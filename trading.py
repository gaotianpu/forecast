#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
from datetime import datetime,date,timedelta

import random


def load_dates_stock(stock_no,buy_date,hold_days):    
    r = dbr.select('stock_daily_records',
        where="stock_no=$stock_no and volume>0 and date>=$buy_date", offset=0,limit=hold_days+1,order="date asc", vars=locals())
    return list(r)

def buy_and_sell(strategy_id,strategy_batch_no,stock_no,buy_date,hold_days,buy_price='open_price',sell_price='open_price',trade_hands=1):
    stocks = load_dates_stock(stock_no,buy_date,hold_days)    
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

def run_strategy_sum():
    pass 
##################################


def run(strategy,stocks,hold_days=1):    
    stocks_count = len(stocks) 
    if stocks_count < 1000:
        for i in range(stocks_count):
            buy_sell(i,stocks[i],hold_days) 
    else :
        for i in range(1000):
            buy_sell(i,random.choice(stocks),hold_days) 


if __name__ == "__main__":
    buy_and_sell(1,1,600000,'2013-09-23',1)
    #print random.randrange(1000)
    #run(filter_stocks_func,strategy,date)


