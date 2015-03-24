#!/usr/bin/python
# -*- coding: utf-8 -*-
import redis
import config
import loader
# 使用redis,把每日获取的每个股票，分拆到各股票中 
# 

red = redis.StrictRedis(host='localhost')

def push_all_history():
    stocks = load_all_stocks()
    for stock in stocks:
        push_history(stock)

def push_history(stock):
    x = stock.split('.')
    k = x[1].replace('ss','sh') +  x[0]
    red.delete(k)    
    records = loader.load_stock_history(stock)
    for r in records:         
        red.lpush(k,r) 

def push_records(day):
    stocks = loader.load_daily_stocks(day)
    for k,v in stocks.items():
        red.lpush(k,v) 


if __name__ == "__main__":
    latest_day = config.get_today()
    # push_history('600000.ss')

    print red.lrange('sh600000',0,10)
    # push_records('2015-03-23')
    # red.set('a','abc')
    # print red.get('a')
    # print red.delete('a')
    # print red.get('a')
