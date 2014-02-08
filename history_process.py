#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import os
from config import dbr,dbw,const_root_local,init_log
import comm
import multiprocessing
import csv
from decimal import *

def parse_history_data(lfile):
    l=[]
    with open(lfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for date,openp,high,low,close,volume,acp in reader:
            if date == 'Date': continue
            r = web.storage(date=date,open=Decimal(openp),high=Decimal(high),
                low=Decimal(low),close=Decimal(close),acp=Decimal(acp),volume=int(volume),)            
            l.append(r)
    return l

def process(filename):
    fullpath = '%s/dailyh/%s' % (const_root_local,filename)
    records = parse_history_data(fullpath)
    count = len(records)
    for i in range(0,count):
        records[i].last_close = 0 
        records[i].lacp = 0         
        if (count-i) > 1: 
            records[i].last_close =  records[i+1].close
            records[i].lacp =  records[i+1].acp
        print records[i]

def _____drop_multi_run(filename):
    ##须有最大进程数限制
    multiprocessing.Process(name=filename,target=process,args=(filename,)).start()     
    # worker_1 = multiprocessing.Process(name='worker 1',target=process,args=(filename,))  
    # worker_1.start()   

def run():  
    local_dir = "%s/dailyh/"  % (const_root_local)   
    filenames = os.listdir(local_dir)
    mpPool = multiprocessing.Pool(processes=20)
    for f in filenames:     
        mpPool.apply_async(process,(f,))        
    mpPool.close()
    mpPool.join()


if __name__ == "__main__":
    process('300001.sz.csv')
    #run()