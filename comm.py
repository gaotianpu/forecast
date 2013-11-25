#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import re
from decimal import *
import web

def is_trade_day():
    #不包含工作日
    return datetime.datetime.now().weekday() not in (5,6)

def is_trade_time():
    if not is_trade_day():
        return False
    current_hhmm = int(datetime.datetime.now().strftime('%Y%m%d%H%M')[8:])
    return not (current_hhmm < 930 or current_hhmm > 1510 or (current_hhmm>1140 and current_hhmm<1300 ))

##解析每日数据
def parse_daily_data(lfile):
    #file exit?
    with open(lfile,'rb') as f:
        lines = f.readlines()
        f.close()

    rows=[]
    regex = re.compile("_[a-z]{2}([\d]+)=")
    for a in lines:
        fields = a.split(',')
        if(len(fields)<30):continue

        stockno = regex.findall(fields[0])
        if not stockno: break

        last_close = fields[2]
        close_price = fields[3]

        raise_drop = Decimal(close_price) - Decimal(last_close)
        raise_drop_rate = raise_drop / Decimal(last_close) if Decimal(last_close) != 0 else 0

        r = web.storage(stock_no=stockno[0],open_price=fields[1],high_price=fields[4],
            low_price=fields[5],close_price=close_price,last_close=last_close,
            volume=int(fields[8]),amount=fields[9] ,
            raise_drop=raise_drop, raise_drop_rate=raise_drop_rate,
            is_new_high = fields[4]==fields[3],
            is_new_low = fields[5]==fields[3],
            date=fields[30],time=fields[31])

        #print r
        rows.append(r)
    #rows = [r for r in rows if r['new_high'] ]  当前价就是今天的最高价
    return rows

import csv
def parse_history_data(lfile):
    l=[]
    with open(lfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for date,openp,highp,lowp,closep,volume,adjclose in reader:
            if date == 'Date' or volume=='000':
                continue
            r = web.storage(date=date,open_price=openp,high_price=highp,low_price=lowp,close_price=closep,volume=volume)
            print r
            l.append(r)
    return l


if __name__ == '__main__':
    parse_history_data('D:\\gaotp\\stocks\\dailyh\\000001.sz.csv')
    #print is_trade_time()

