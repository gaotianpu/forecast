#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
from config import dbr,dbw
import comm

def getFutureRange(prate):
    if prate>10:  #1%
        return 2
    if prate<=10:
        return 1
    return 0

    # if prate < -20: #-2%
    #     return 1 
    # if prate<=10 and prate>=-20:
    #     return 2
    # return 0    

def computeFuture(records):
    for r in records:
        i = records.index(r)        
        if i>1:
            prate = int((records[i-2].close - records[i-1].close) *1000 / records[i-1].close)
            frange = getFutureRange(prate)
            sql = 'update stock_daily set future1_prate=%s,future1_range=%s where pk_id=%s' % (prate,frange,r.pk_id) 
            dbw.query(sql)
        if i>2:
            prate = int((records[i-3].close - records[i-1].close) *1000 / records[i-1].close )
            frange = getFutureRange(prate)
            sql = 'update stock_daily set future2_prate=%s,future2_range=%s where pk_id=%s' % (prate,frange,r.pk_id)  
            dbw.query(sql)            
        if i>3:
            prate = int((records[i-4].close - records[i-1].close) *1000 / records[i-1].close )
            frange = getFutureRange(prate)
            sql = 'update stock_daily set future3_prate=%s,future3_range=%s where pk_id=%s' % (prate,frange,r.pk_id) 
            dbw.query(sql)

def computeTrend(records):
    count = len(records)
    for i in range(0,count):        
        if count-i>2:
            t3 = comm.get_trend(records[i:i+3])
            sql = 'update stock_daily set trend_3=%s where pk_id=%s' % (t3,records[i].pk_id) 
            dbw.query(sql)
        if count-i>4:
            t5 = comm.get_trend(records[i:i+5])
            sql = 'update stock_daily set trend_5=%s where pk_id=%s' % (t5,records[i].pk_id) 
            dbw.query(sql) 

def computeVolume(records):
    count = len(records)
    for i in range(0,count):   
        r10 = records[i:i+10]        
        l = [r.volume for r in r10]
        volume_avg_10 = reduce(lambda x, y: x + y, l) / len(l)
        volume_p = float(records[i].volume) / volume_avg_10
        
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

        sql = 'update stock_daily set volume_avg_10=%s,volume_level=%s where pk_id=%s' % (volume_avg_10,volume_level,records[i].pk_id) 
        dbw.query(sql)  

def computeCandle(records):
    count = len(records)
    for i in range(0,count):
        r = records[i]
        result = comm.get_candle_2(r.open,r.close,r.high,r.low)
        up_or_down = 2 if result[1]>0 else 1
        sql = 'update stock_daily set candle_sort=%s,up_or_down=%s where pk_id=%s' % (result[4],up_or_down,records[i].pk_id) 
        dbw.query(sql) 

def computeJump(records):
    count = len(records)
    for i in range(0,count):
        if count-i==2:break
        last_price = records[i+1].last_close 
        open_last_close = records[i].open - last_price 
        jump_rate = open_last_close / last_price 
        jump_level = 0 

        if jump_rate*100>=2:
            jump_level = 3
        elif jump_rate*100>=0 and jump_rate*100<2:
            jump_level = 2
        elif jump_rate*100<0:
            jump_level = 1
        else:
            jump_level = 50 

        sql = 'update stock_daily set jump_level=%s,jump_rate=%s where pk_id=%s' % (jump_level,jump_rate,records[i].pk_id) 
        dbw.query(sql) 

def computeMA(records):
    count = len(records)
    for i in range(0,count):
        ma5 = ma10 = 0
        if count-i>=5:
            l5 = [r.close for r in records[i:i+5]]
            ma5 = reduce(lambda x, y: x  + y , l5) / 5           
        if count-i>=10:
            l10 = [r.close for r in records[i:i+10]]
            ma10 = reduce(lambda x, y: x  + y , l10) / 10
        ma_5_10 = 0
        if ma5<>0 and ma10<>0:
            ma_5_10 = 2 if ma5>ma10 else 1 
        sql = 'update stock_daily set ma_5=%s,ma_10=%s,ma_5_10=%s where pk_id=%s' % (ma5,ma10,ma_5_10,records[i].pk_id) 
        dbw.query(sql)      

import test2
def computeForecast(records,categories,allpp):
    count = len(records)
    for i in range(0,count):
        if not records[i].trend_3:
            continue   
        if not records[i].trend_5:
            continue 
        if not records[i].candle_sort:
            continue         
        if not records[i].up_or_down:
            continue
        if not records[i].volume_level:
            continue
        if not records[i].jump_level:
            continue
        if not records[i].ma_5_10:
            continue
        fields = {'trend_3':records[i].trend_3,
        'trend_5':records[i].trend_5,
        'candle_sort':records[i].candle_sort,
        #'up_or_down':records[i].up_or_down,
        'volume_level':records[i].volume_level
        ,'jump_level':records[i].jump_level
        ,'ma_5_10':records[i].ma_5_10
        }
        #print fields
        x = test2.run(fields,categories,allpp)
        sql = 'update stock_daily set forecast=%s where pk_id=%s' % (x[2]/x[1],records[i].pk_id) 
        dbw.query(sql)     

def computeLastClosePrice(records):
    count = len(records)
    for i in range(0,count):
        if (count-i) == 1:
            break
        last_close = records[i+1].close
        open_last_close = records[i].open - records[i+1].close
        high_low = records[i].high - records[i].low
        close_open = records[i].close - records[i].open
        price_rate = (records[i].close - last_close)/last_close
        high_rate = (records[i].high - last_close)/last_close
        low_rate = (records[i].low - last_close)/last_close
        high_low_rate = high_rate - low_rate
        candle = comm.get_candle_2(records[i].open,records[i].close,records[i].high,records[i].low)
        range_1 = candle[0]
        range_2 = candle[1]
        range_3 = candle[2]
        pk_id = records[i].pk_id
        dbw.update('stock_daily',high_low=high_low,last_close=last_close,open_last_close=open_last_close,
            price_rate=price_rate,high_rate=high_rate,low_rate=low_rate,hig_low_rate=high_low_rate,
            range_1 = range_1,range_2 = range_2,range_3 = range_3,
            where="pk_id=$pk_id",vars=locals())

             
def run_all():
    categories = test2.getCategories()
    allpp = test2.loadP() 

    stocks = da.stockbaseinfos.load_all_stocks()  
    for s in stocks:
        print s.stock_no         
        stock_daily_records = da.stockdaily.load_stockno(s.stock_no)
        computeLastClosePrice(stock_daily_records)        
        computeFuture(stock_daily_records)
        computeTrend(stock_daily_records)
        computeCandle(stock_daily_records)
        computeVolume(stock_daily_records)
        computeJump(stock_daily_records)
        computeMA(stock_daily_records)
        computeForecast(stock_daily_records,categories,allpp)
        break


if __name__ == '__main__':
    run_all()