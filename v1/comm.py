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
    
    #print open,close,high,low

    if open==0 : return (0,0,0,0,0)

    hl = high-low
    if hl==0:
        return (0,0,0,0,0)
    rang_top = (high-close)/hl if close-open > 0  else (high-open)/hl
    rang_middle = (close - open)/hl  
    rang_bottom = (open-low)/hl if close-open > 0  else (close-low)/hl

    candleSort = []
    candleSort.append('9' if rang_top>=0.15 else '6') 
    candleSort.append('9' if abs(rang_middle)>=0.15 else '6') 
    candleSort.append('9' if rang_bottom>=0.15 else '6')

    #tmp = int(''.join(candleSort))
    #tmp = int(tmp) if rang_middle>0 else 0-int(tmp)
    return (int((round(rang_top*10))),int((round(rang_middle*10))),int((round(rang_bottom*10))),
        high-low,int(''.join(candleSort)))

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
                candle = get_candle_data(openp,closep,highp,lowp),
                candle_2 = get_candle_2(openp,closep,highp,lowp) )
            #print r
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

def get_trend_2(rows,fieldName):
    rows = sorted(rows, cmp=lambda x,y : cmp(x[fieldName], y[fieldName]))

    i=1
    for r in rows:
        r.index = i
        i = i + 1

    t=''
    rows = sorted(rows, cmp=lambda x,y : cmp(x.trade_date, y.trade_date))
    for r in rows:
        t = t + str(r.index)

    return int(t) 

def get_volume_level(volume_p):
    #对volume进行分类
    volume_level = 0 
    if volume_p>=3:
        volume_level = 31
    elif volume_p<3 and volume_p>=2:
        volume_level = 21
    elif volume_p<2 and volume_p>=0.5:
        volume_level = 19
    elif volume_p<0.5 and volume_p>=0.33:
        volume_level = 12
    elif volume_p<0.33:
        volume_level = 13
    else:
        volume_level = 0 
    return volume_level

def get_jump_level(jump_rate):
    jump_level = 0
    if jump_rate*100>=2:
        jump_level = 3
    elif jump_rate*100>=0 and jump_rate*100<2:
        jump_level = 2
    elif jump_rate*100<0:
        jump_level = 1
    else:
        jump_level = 50
    return jump_level  

def getFutureRange(prate):
    if prate<=-0.02:
        return 1  #'bear' #熊
    elif prate > 0.02:   
        return 3 #'bull' #牛
    else:
        return 2 #'snake' #震荡

def get_ma(records,index):
    daysC=[5,10,20,50,100,200]
    d={}
    rows=[]
    for days in daysC:
        l = [r.close for r in records[index:index+days]]
        maP = reduce(lambda x, y: x  + y , l) / len(l)
        rows.append([days,maP])
        d['ma_%s'%(days)] = maP 

    for i in range(2,6):
        tmp = rows[0:i]
        tmp = sorted(tmp, cmp=lambda x,y : cmp(y[1], x[1])) 
        d['ma_p_%s'%(i)] = '_'.join([str(r[0]) for r in tmp]) 
        
    return d

def get_peak_trough(records,count,index,days): 
    if index<days: return 0
    if index+days+1 > count : return 0

    left_records = records[index+1:index+days+1] if index+days+1 <  count else records[index+1:]
    right_records = records[index-days:index]  if index>days else records[:index]
    current_record = records[index]
     
    peak = True #波峰
    trough = True #波谷
    for r in left_records:        
        trough = trough and r.close>current_record.close
        peak = peak and r.close < current_record.close    

    for r in right_records:        
        trough = trough and r.close>current_record.close
        peak = peak and r.close < current_record.close 
    if trough: return 1
    if peak: return  2
    return 0

def fix_peak_trough(records,peak_trough_field):     
    peak_trough_nodes = [r for r in records if r[peak_trough_field] <> 0]
    rows = []
    count = len(peak_trough_nodes)
    for i in range(0,count):
        if i > count-2: break
        r = peak_trough_nodes[i]
        if peak_trough_nodes[i][peak_trough_field] == peak_trough_nodes[i+1][peak_trough_field]:
            rows.append(web.storage(peak_trough=r[peak_trough_field],begin=peak_trough_nodes[i+1].trade_date,end=r.trade_date) )
     
    # for pt in rows:
    #     tmpl = [r for r in records if r.trade_date>pt.begin and r.trade_date<pt.end] 
    #     tmpl = sorted(tmpl, cmp=lambda x,y : cmp(x.close, y.close))
    #     new_node = tmpl[-1] if pt.peak_trough==1 else tmpl[0]         
    #     i = records.index(new_node)
    #     records[i][peak_trough_field] = 1 if pt.peak_trough==2 else 2

    tmpl = sorted(records, cmp=lambda x,y : cmp(x.trade_date, y.trade_date))
    peak_trough = 0 
    index = 0 
    for r in tmpl:
        pass
        # print '%s,%s,%s,%s,%s' %(r.trade_date,r.volume,r.close,r.ma_5,r[peak_trough_field] )
        # if r[peak_trough_field]<>0:
        #     peak_trough = r[peak_trough_field] )
        #     index = tmpl.index(r)   
         
        # if (tmpl.index(r)-index)==2:
        #     print '%s,%s,%s' %(r.trade_date,'buy' if peak_trough==1 else 'sell',r.close)         
        # print r.trade_date,r.close,r[peak_trough_field],index,tmpl.index(r),tmpl.index(r)-index    

    # peak_trough = 0  
    # for r in records:
    #     if  r[peak_trough_field]:
    #         peak_trough = r[peak_trough_field] 
    #     tmp = ''
    #     if peak_trough==0:
    #         tmp = 'unknown'
    #     elif peak_trough==1:
    #         tmp = 'down'
    #     else:
    #         tmp = 'up'           
    #     print '%s,%s,%s,%s,%s' %(r.trade_date,r.close,r.future1_range,r[peak_trough_field],tmp) 

    return  records   

def get_test(records,index):
    days = 100
    last_records = records[index:index+days]   
    if len(last_records) == 100:
        tmpl = sorted(last_records, cmp=lambda x,y : cmp(x.close, y.close))
        max_record = tmpl[-1] 
        min_record = tmpl[0]
        # print records[index].trade_date,records[index].close,max_record.close-records[index].close/max_record.close
        # if max_record.trade_date == records[index].trade_date:
        #     # print min_record.trade_date,min_record.close
        #     tmpl = sorted(tmpl, cmp=lambda x,y : cmp(x.trade_date, y.trade_date))
        #     min_index = tmpl.index(min_record)
        #     tmpll = sorted(tmpl[:min_index], cmp=lambda x,y : cmp(x.close, y.close))
        #     #print len(tmpll), '#',tmpll[-1].trade_date, tmpll[-1].close
        #     print min_index,records[index].trade_date, min_record.trade_date,max_record.close,min_record.close
        #     #tmpl[0].trade_date,tmpl[1].trade_date, tmpl[0].close, tmpl[-1].close

        # print len(last_records),records[index].trade_date,tmpl[0].trade_date,tmpl[1].trade_date, tmpl[0].close, tmpl[-1].close


def get_prices(high,low):
    l = []
    l.append(low)     
    for i in range(int(low*100),int(high*100)):
        l.append(float(i)/100) 
    l.append(high)
    return l

import math
def cos_dist(a):
    b = [1,1,1,1,1]
    if len(a) != len(b):
        return None
    part_up = 0.0
    a_sq = 0.0
    b_sq = 0.0
    for a1, b1 in zip(a,b): #zip , 2+ list -> tuple list
        part_up += a1*b1
        a_sq += a1**2
        b_sq += b1**2
    part_down = math.sqrt(a_sq*b_sq) #sqrt
    if part_down == 0.0:
        return None
    else:
        return part_up / part_down

if __name__ == '__main__':
    l=[1,2,3,4,5]
    print l[:2]
    print l[2:]
    # get_market_codes('0024556')
    # get_market_codes('0004556')
    # get_market_codes('3004556')
    # get_market_codes('6004556')
    #parse_daily_data('D:\\gaotp\stocks\\daily\\20131125_0.txt')
    #parse_history_data('D:\\gaotp\\stocks\\dailyh\\000001.sz.csv')
    #print is_trade_time()

