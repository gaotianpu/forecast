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
import datetime

############读写数据 ####################
def add_new_record(r):  
    stock_no  = '%s.%s' % (r.stock_no,r.market_codes.yahoo)  
    rows = load_raw_records(stock_no)
    rows.insert(0,web.storage(trade_date=r.date,open=r.open_price,high=r.high_price,
                low=r.low_price,close=r.close_price,acp=r.close_price,volume=r.volume)) 
    write_raw_records(stock_no,rows)
    

def write_raw_records(stock_no,rows):
    #rows去掉重复项后重新排序
    #rows = list(set(rows))
    rows = sorted(rows, cmp=lambda x,y : cmp(y.trade_date, x.trade_date))
    content = 'Date,Open,High,Low,Close,Volume,Adj Close\n'       
    content = content + '\n'.join(['%s,%s,%s,%s,%s,%s,%s' % (r.trade_date,r.open,r.high,r.low,r.close,r.volume,r.close) for r in rows])
    content = content + '\n'

    lfile = '%s/dailyh/%s.csv' % (const_root_local,stock_no) 
    with open(lfile, 'w') as f:
        f.write(content)

def load_raw_records(stock_no):
    lfile = '%s/dailyh/%s.csv' % (const_root_local,stock_no)      
    l=[]
    if not os.path.isfile(lfile):
        return l
    with open(lfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for date,openp,high,low,close,volume,acp in reader:
            if date == 'Date': continue
            r = web.storage(trade_date=date,open=float(openp),high=float(high),
                low=float(low),close=float(close),acp=float(acp),volume=int(volume),)            
            l.append(r)
        f.close()
    l = [r for r in l if r.volume>0]
    l = sorted(l, cmp=lambda x,y : cmp(y.trade_date, x.trade_date))
    return l

def load_stocks_rawdata(trade_date):
    lfile = "%s/daily_/%s.csv"  % (const_root_local,trade_date) 
    d = {}
    with open(lfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for py,stock_no,openp,close,high,low,volume in reader:
            if not int(volume): continue
            d[stock_no] = web.storage(stock_no=stock_no,open=float(openp),high=float(high),
                low=float(low),close=float(close),volume=int(volume),)
    return d   

###读写处理过的stock数据     
def save_stocks(stock_no,records):
    lfile = '%s/dailyh_add/%s.csv' % (const_root_local,stock_no) 
    content = '\n'.join([json.dumps(r) for r in records])       
    with open(lfile, 'w') as file: 
        file.write(content)

def load_stocks(stock_no): 
    lfile = '%s/dailyh_add/%s.csv' % (const_root_local,stock_no)      
    rows=[] 
    with open(lfile,'rb') as f:
        lines = f.readlines()
        rows = [web.storify(json.loads(line.strip())) for line in lines if line] 
    rows = [r for r in rows if int(r['volume'])>0]    
    return rows

###读写处理过的stock categroy,features的sum数据   
def save_sum_records(stock_no,content):
    new_filepath = '%s/dailyh_sum/%s.csv' % (const_root_local,stock_no)    
    with open(new_filepath, 'w') as file: 
        file.write(content)

def load_sum_records(stock_no):
    fullpath = '%s/dailyh_sum/%s.csv' % (const_root_local,stock_no)
    l=[] 
    with open(fullpath,'rb') as f:
        reader = csv.reader(f, delimiter=',')            
        for fk,cv,fv,count,p in reader:
            l.append(web.storage(fk=fk,cv=cv,fv=fv,count=count,p=p))
    return l

##读写Category,Feature概率
def save_probability(content):
    new_filepath = '%s/dailyh_final/cfp.csv' % (const_root_local)    
    with open(new_filepath, 'w') as file: 
        file.write(content) 

def load_probability(): 
    pfile = '%s/dailyh_final/cfp.csv' % (const_root_local) 
    l = []  
    with open(pfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for key,count,probability in reader:
            segments = key.split('|')
            if len(segments)==3:
                l.append(web.storage(fk=segments[0],fv=segments[2],cv=segments[1],p=probability,count=count))
            elif len(segments)==2:
                l.append(web.storage(fk='category',fv='',cv=segments[1],p=probability,count=count))
            else:                
                pass #print '--',key,count,probability
    return l

####
def gen_date_file(record):
    json_record = json.dumps(record)
    new_filepath = '%s/dailyh_dates/%s.csv' % (const_root_local,record.trade_date) 
    with open(new_filepath, 'ab+') as file: 
            file.write(json_record+'\n') 

def gen_date_files(trade_date):
    path = '%s/dailyh_add/' % (const_root_local)  
    filenames = os.listdir(path)
    
    l=[]    
    for f in filenames:
        stock_no = '.'.join(f.split('.')[0:2])
        print stock_no
        records = load_stocks(stock_no)
        date_record = [r for r in records if r.trade_date==trade_date]
        if date_record:
            l.append(date_record[0])
    
    # l = sort(l, cmp=lambda x,y : cmp(x.trade_date, y.trade_date))
            
    lfile = '%s/dailyh_dates/%s.csv' % (const_root_local,trade_date)         
    content = '\n'.join([json.dumps(r) for r in l])       
    with open(lfile, 'w') as file: 
        file.write(content) 

def load_date(trade_date):
    lfile = '%s/dailyh_dates/%s.csv' % (const_root_local,trade_date)      
    rows=[] 
    with open(lfile,'rb') as f:
        lines = f.readlines()
        rows = [web.storify(json.loads(line.strip())) for line in lines if line] 
    rows = [r for r in rows if int(r['volume'])>0]    
    return rows

#############################################
def write_reports(stock_no,fields):
    records = load_stocks(stock_no)
    #需验证fields出现的字段，是否在records里出现
    l=[]
    for r in records:
        l.append(','.join([ str(r[f]) for f in fields]))

    lfile = '%s/reports/%s.%s.csv' % (const_root_local,stock_no,'.'.join(fields))         
    content = '\n'.join(l)
    with open(lfile, 'w') as file: 
        file.write(content) 


if __name__ == "__main__":
    write_reports('000006.sz',['trade_date','close'])