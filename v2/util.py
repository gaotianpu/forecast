#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

def get_today():
    today = datetime.datetime.now()
    trade_date = today.strftime('%Y-%m-%d')
    return trade_date

def is_trade_day():
    if datetime.datetime.today().weekday() not in [0,1,2,3,4]: return False
    if get_today() in ['2015-05-01'] : return False
    return True


