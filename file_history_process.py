#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import os
from config import dbr,dbw,const_root_local,init_log
import comm
import multiprocessing
import csv
from decimal import *
import json

def parse_history_data(lfile):
    l=[]
    with open(lfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for date,openp,high,low,close,volume,acp in reader:
            if date == 'Date': continue
            r = web.storage(trade_date=date,open=float(openp),high=float(high),
                low=float(low),close=float(close),acp=float(acp),volume=int(volume),)            
            l.append(r)
    return l

def process(filename):    
    fullpath = '%s/dailyh/%s' % (const_root_local,filename)
    
    records = parse_history_data(fullpath)
    count = len(records)    
    for i in range(0,count):
        records[i].high_low = records[i].high - records[i].low
        records[i].close_open = records[i].close - records[i].open 
        
        records[i].jump_level = 0
        if (count-i) > 1: 
            records[i].last_close =  records[i+1].close  
            records[i].last_acp =  records[i+1].acp  
            records[i].open_lastclose = records[i].open - records[i].last_close  
            records[i].jump_rate = records[i].open_lastclose / records[i].last_close  
            records[i].jump_level = comm.get_jump_level(records[i].jump_rate)
            records[i].price_rate = (records[i].close - records[i].last_close) / records[i].last_close  
            records[i].high_rate = (records[i].high - records[i].last_close) / records[i].last_close  
            records[i].low_rate = (records[i].low - records[i].last_close) / records[i].last_close  
            records[i].hig_low_rate = records[i].high_rate - records[i].low_rate  

        candles = comm.get_candle_2(records[i].open,records[i].close,records[i].high,records[i].low)
        records[i].range_1 = candles[0]
        records[i].range_2 = candles[1]
        records[i].range_3 = candles[2]
        records[i].candle_sort  = candles[4]
        records[i].up_or_down = 2 if candles[1]>0 else 1

        r10 = records[i:i+10]        
        l = [r.volume for r in r10]
        volume_avg_10 = reduce(lambda x, y: x + y, l) / len(l)
        volume_p = float(records[i].volume) / volume_avg_10  if volume_avg_10 else 0
        records[i].volume_avg_10 = volume_avg_10
        records[i].volume_level = comm.get_volume_level(volume_p)

                   
        records[i].trend_3 = comm.get_trend(records[i:i+3]) if count-i>2 else 0                    
        records[i].trend_5 = comm.get_trend(records[i:i+5]) if count-i>4 else 0

        l5 = [r.close for r in records[i:i+5]]
        ma5 = reduce(lambda x, y: x  + y , l5) / 5
        l10 = [r.close for r in records[i:i+10]]
        ma10 = reduce(lambda x, y: x  + y , l10) / 10
        ma_5_10 = 0
        if ma5<>0 and ma10<>0:
            ma_5_10 = 2 if ma5>ma10 else 1 
        records[i].ma_5 = ma5
        records[i].ma_10 = ma10
        records[i].ma_5_10 = ma_5_10

        if i>1:
            prate = int((records[i-2].close - records[i-1].close) *1000 / records[i-1].close)
            frange = comm.getFutureRange(prate) 
            records[i].future1_prate = prate
            records[i].future1_range = frange  
        if i>2:
            prate = int((records[i-3].close - records[i-1].close) *1000 / records[i-1].close )
            frange = comm.getFutureRange(prate)
            records[i].future2_prate = prate
            records[i].future2_range = frange
        if i>3:
            prate = int((records[i-4].close - records[i-1].close) *1000 / records[i-1].close )
            frange = comm.getFutureRange(prate)
            records[i].future3_prate = prate
            records[i].future3_range = frange    
        #print records[i]  
    
    mapfn(filename,records)   
     
    content = '\r'.join([json.dumps(r) for r in records])
    new_filepath = '%s/dailyh_add/%s' % (const_root_local,filename)    
    with open(new_filepath, 'w') as file: 
        file.write(content)
    print filename

def process_callback():
    pass

categoryField = 'future1_range'
featureFields =('trend_3','trend_5','candle_sort','up_or_down','volume_level','jump_level','ma_5_10')    
from collections import Counter
def mapfn(filename,records):
    l = []
    total_count = len(records)
    trade_records = [r for r in records if r.volume>0]
    trade_count = len(trade_records)
    categories = dict(Counter(r[categoryField] for r in trade_records))

    l.append('total:%s'%(total_count))
    l.append('trade:%s'%(trade_count))     
    for k,v in categories.items():
        l.append('category_%s:%s'%(k,v))   
    
    for fk in featureFields:
        for ck,cv in categories.items(): 
            cfvalues =dict(Counter('%s|%s|%s' % (fk,r[categoryField],r[fk]) for r in trade_records))
            for k,v in cfvalues.items():
                l.append('%s:%s' % (k,v)  )
          
    content = '\r\n'.join(l)
    new_filepath = '%s/dailyh_sum/%s' % (const_root_local,filename)    
    with open(new_filepath, 'w') as file: 
        file.write(content)

import csv
def reducefn():
    local_dir = "%s/dailyh_sum/"  % (const_root_local)   
    filenames = os.listdir(local_dir)

    d = {}
    for f in filenames:
        fullpath = '%s/dailyh_sum/%s' % (const_root_local,f) 
        with open(fullpath,'rb') as f:
            reader = csv.reader(f, delimiter=':')
            for k,v in reader:                 
                d[k] = d[k]+v if k in d else 0

    content = '\r\n'.join(['%s,%s' % (k,v)  for k,v in d.items()])
    new_filepath = '%s/dailyh_final/1.txt' % (const_root_local)    
    with open(new_filepath, 'w') as file: 
        file.write(content)

def _____drop_multi_run(filename):
    ##须有最大进程数限制
    multiprocessing.Process(name=filename,target=process,args=(filename,)).start()     
    # worker_1 = multiprocessing.Process(name='worker 1',target=process,args=(filename,))  
    # worker_1.start()   

def run():  
    local_dir = "%s/dailyh/"  % (const_root_local)   
    filenames = os.listdir(local_dir)
    mpPool = multiprocessing.Pool(processes=3)
    for f in filenames:     
        mpPool.apply_async(process,(f,))        
    mpPool.close()
    mpPool.join()


if __name__ == "__main__":
    run()
    #process('300003.sz.csv')
    reducefn()
    
    