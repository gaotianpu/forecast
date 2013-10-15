#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
import random


def buy_sell(strategy_id=1,strategy_batch_no=1,stock,hold_days,buy_time='open',sell_time='close',hands=10):
   

    next_day_stock = load_next_day_stock(stock.stock_no,stock.date,hold_days)
    #strategy_id,strategy_batch_no,date,stock_no,open_or_close,-price,earnings,earn_rate 
    #strategy_id,strategy_batch_no,date,stock_no,open_or_close,+price,earnings,earn_rate
    dbw.insert('trading_records',
        strategy_id=strategy_id,
        strategy_batch_no=strategy_batch_no,
        stock_no=stock.stock_no,
        date = stock.date,
        open_or_close=buy_time,
        price=(0-price),
        earnings=earnings,earn_rate=earn_rate)

    #date, load stocks by rules
    #random choice one 
    #open or close price ?
    #trade_batch_no
    #insert tradding_records

    #hold days
    #get that day stock
    #open or close price 
    #insert tradding_records

    #how much 



def load_stocks(date):
    return list(dbr.select('stock_daily_records',where="date=$date",offset=0,limit=10,vars=locals()))

def load_next_day_stock(stock_no,date,hold_days):
    r = dbr.select('stock_daily_records',
        where="stock_no=$stock_no and volume>0 and date>$date",
        order="date desc",
        offset=0,limit=hold_days,
        vars=locals())
    return r[0]

def run(strategy,stocks,hold_days=1):    
    stocks_count = len(stocks) 
    if stocks_count < 1000:
        for i in range(stocks_count):
            buy_sell(i,stocks[i],hold_days) 
    else :
        for i in range(1000):
            buy_sell(i,random.choice(stocks),hold_days) 


if __name__ == "__main__":
    print random.randrange(1000)
    #run(filter_stocks_func,strategy,date)