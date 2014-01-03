#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import re
from decimal import *
import web

def is_trade_day():
    #不包含工作日
    tday = datetime.datetime.now().weekday() not in (5,6)
    return tday

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

        last_close = Decimal(fields[2])
        close_price = Decimal(fields[3])

        raise_drop = close_price - last_close
        raise_drop_rate = raise_drop / last_close if last_close != 0 else 0
        stock_name = fields[0].split('"')[1].decode('gbk').encode("utf-8")

        r = web.storage(stock_no=stockno[0],open_price=fields[1],high_price=fields[4],
            low_price=fields[5],close_price=close_price,last_close=last_close,
            volume=int(fields[8]),amount=fields[9] ,
            raise_drop=raise_drop, raise_drop_rate=raise_drop_rate,
            high_low = Decimal(fields[4]) - Decimal(fields[5]) ,
            close_open = close_price - Decimal(fields[1]) ,
            open_last_close = Decimal(fields[1]) - last_close,
            is_new_high = fields[4]==fields[3],
            is_new_low = fields[5]==fields[3],
            jump_rate =  (Decimal(fields[1]) - last_close)/last_close,
            high_rate = (Decimal(fields[4]) - last_close)/last_close,
            low_rate = (Decimal(fields[5]) - last_close)/last_close,
            date=fields[30],time=fields[31],
            candle = get_candle_data(fields[1],close_price,fields[4],fields[5]),
            candle_2 = get_candle_2(fields[1],close_price,fields[4],fields[5]),
            market_codes = get_market_codes(stockno[0]) )

        #print r
        rows.append(r)
    #rows = [r for r in rows if r['new_high'] ]  当前价就是今天的最高价
    return rows

def get_candle_2(open,close,high,low):
    open = float(open)
    close = float(close)
    high = float(high)
    low = float(low)
    
    print open,close,high,low

    if open==0 : return (0,0,0)

    hl = high-low
    if hl==0:
        return (0,0,0,0)
    rang_top = (high-close)/hl if close-open > 0  else (high-open)/hl
    rang_middle = (close - open)/hl  
    rang_bottom = (open-low)/hl if close-open > 0  else (close-low)/hl

    return (int((round(rang_top*10))),int((round(rang_middle*10))),int((round(rang_bottom*10))),high-low)

def get_candle_data(open,close,high,low):
    open = float(open)
    close = float(close)
    high = float(high)
    low = float(low)

    if open==0 : return 0

    hl = (high-low)*0.1
    #print open,close,high,low,hl
    if hl==0:
        return 0
    #print  (high-close)/(high-low), str(int(round((high-close)/hl)))

    result = 0
    if close>open:
        result = str(int(round((high-close)/hl)))+ str(int(round((close-open)/hl)))+ str(int(round((open-low)/hl)))
        result = int(result)
    else:
        result = str(int(round((high-open)/hl))) + str(int(round((open-close)/hl)))+ str(int(round((close-low)/hl)))
        result = -int(result)
    return result

import csv
def parse_history_data(lfile):
    l=[]
    with open(lfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for date,openp,highp,lowp,closep,volume,adjclose in reader:
            if date == 'Date' or volume=='000':
                continue
            r = web.storage(date=date,open_price=openp,high_price=highp,low_price=lowp,close_price=closep,volume=volume,
                candle = get_candle_data(openp,closep,highp,lowp))
            print r
            l.append(r)
    return l

def get_market_codes(stock_no):
    #深圳股票代码“002”开头的是中小板，“000”开头的是主板，“3”开头的是创业板；上海股票代码“6”开头的，全部的上海股票都为主板
    if stock_no[:3]=='002':
        return web.storage(yahoo='sz',plate='zxb',pinyin='sz')
    if stock_no[:3]=='000':
        return web.storage(yahoo='sz',plate='sa',pinyin='sz')
    if stock_no[:1]=='3':
        return web.storage(yahoo='sz',plate='cyb',pinyin='sz')
    if stock_no[:1]=='6':
        return web.storage(yahoo='ss',plate='ha',pinyin='sh')
    return web.storage(yahoo='',plate='',pinyin='')


def get_trend(rows):
    rows = sorted(rows, cmp=lambda x,y : cmp(x.close, y.close))

    i=1
    for r in rows:
        r.index = i
        i = i + 1

    t=''
    rows = sorted(rows, cmp=lambda x,y : cmp(x.trade_date, y.trade_date))
    for r in rows:
        t = t + str(r.index)

    return int(t) 

if __name__ == '__main__':
    get_market_codes('0024556')
    get_market_codes('0004556')
    get_market_codes('3004556')
    get_market_codes('6004556')
    #parse_daily_data('D:\\gaotp\stocks\\daily\\20131125_0.txt')
    #parse_history_data('D:\\gaotp\\stocks\\dailyh\\000001.sz.csv')
    #print is_trade_time()

