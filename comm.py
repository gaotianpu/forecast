#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

def is_trade_day():
    #不包含工作日
    return datetime.datetime.now().weekday() not in (5,6)

def is_trade_time():
    if not is_trade_day():
        return False
    current_hhmm = int(datetime.datetime.now().strftime('%Y%m%d%H%M')[8:])
    return not (current_hhmm < 930 or current_hhmm > 1510 or (current_hhmm>1140 and current_hhmm<1300 ))


if __name__ == '__main__':
    print is_trade_time()

