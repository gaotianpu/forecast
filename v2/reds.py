#!/usr/bin/python
# -*- coding: utf-8 -*-
import redis
import loader
# 使用redis,把每日获取的每个股票，分拆到各股票中 
# 

red = redis.StrictRedis(host='localhost')

def push_records(day):
    stocks = loader.load_daily_stocks(day)
    for k,v in stocks:
        red.lpush(k,v) 


if __name__ == "__main__":
    red.set('a','abc')
    print red.get('a')