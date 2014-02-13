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

categoryField = 'future1_range'
featureFields =('trend_3','trend_5','candle_sort','up_or_down','volume_level','jump_level','ma_5_10','ma_p_2','ma_p_3','ma_p_4','ma_p_5','close_ma_5','close_ma_10','close_ma_20','close_ma_50','close_ma_100','close_ma_200')  

############读写数据 ####################

def load_raw_records(stock_no):
    lfile = '%s/dailyh/%s.csv' % (const_root_local,stock_no) 
    l=[]
    with open(lfile,'rb') as f:
        reader = csv.reader(f, delimiter=',')
        for date,openp,high,low,close,volume,acp in reader:
            if date == 'Date': continue
            r = web.storage(trade_date=date,open=float(openp),high=float(high),
                low=float(low),close=float(close),acp=float(acp),volume=int(volume),)            
            l.append(r)
    l = [r for r in l if r.volume>0]
    return l

###读写处理过的stock数据     
def save_stocks(stock_no,records):
    lfile = '%s/dailyh_add/%s.csv' % (const_root_local,stock_no) 
    content = '\r\n'.join([json.dumps(r) for r in records])       
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

#############################################

def process1(stock_no):  
    records = load_raw_records(stock_no)
    count = len(records)    
    # print 'trade_date,close,peak5,peak10'   

    for i in range(0,count):        
        records[i].peak_trough_5 = comm.get_peak_trough(records,count,i,3)
        records[i].peak_trough_10 = comm.get_peak_trough(records,count,i,5)

        # current_record = records[i]
        # print '%s,%s,%s,%s' %(current_record.trade_date,current_record.close,records[i].peak_trough_5,records[i].peak_trough_10)


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

        #成交量
        r10 = records[i:i+10]        
        l = [r.volume for r in r10]
        volume_avg_10 = reduce(lambda x, y: x + y, l) / len(l)
        volume_p = float(records[i].volume) / volume_avg_10  if volume_avg_10 else 0
        records[i].volume_avg_10 = volume_avg_10
        records[i].volume_level = comm.get_volume_level(volume_p)
                   
        records[i].trend_3 = comm.get_trend(records[i:i+3]) if count-i>2 else 0                    
        records[i].trend_5 = comm.get_trend(records[i:i+5]) if count-i>4 else 0

        #移动平均线
        MAs = comm.get_ma(records,i)  
        # print MAs       
        ma_5 = records[i].ma_5 = MAs['ma_5']
        ma_10 = records[i].ma_10 = MAs['ma_10']
        records[i].ma_20 = MAs['ma_20']
        records[i].ma_50 = MAs['ma_50']
        records[i].ma_100 = MAs['ma_100']
        records[i].ma_200 = MAs['ma_200']

        records[i].ma_p_2 = MAs['ma_p_2']
        records[i].ma_p_3 = MAs['ma_p_3']
        records[i].ma_p_4 = MAs['ma_p_4']
        records[i].ma_p_5 = MAs['ma_p_5']

        records[i].close_ma_5 = records[i].close > MAs['ma_5']
        records[i].close_ma_10 = records[i].close > MAs['ma_10']        
        records[i].close_ma_20 = records[i].close > MAs['ma_20']
        records[i].close_ma_50 = records[i].close > MAs['ma_50']
        records[i].close_ma_100 = records[i].close > MAs['ma_100']
        records[i].close_ma_200 = records[i].close > MAs['ma_200']

        # for i in range(2,6):
        #     key = 'ma_p_%s' % (i)
        #     records[i][key] = MAs[key] #几条移动平均线的上下关系
        
        ma_5_10 = 0
        if ma_5<>0 and ma_10<>0:
            ma_5_10 = 2 if ma_5>ma_10 else 1 
        records[i].ma_5_10 = ma_5_10

        records[i].future1_prate = 0
        records[i].future1_range = 0
        if i>1:
            prate = (records[i-2].close - records[i-1].close)  / records[i-1].close
            frange = comm.getFutureRange(prate) 
            records[i].future1_prate = prate
            records[i].future1_range = frange
        records[i].future2_prate = 0
        records[i].future2_range = 0  
        if i>2:
            prate = (records[i-3].close - records[i-1].close) / records[i-1].close
            frange = comm.getFutureRange(prate)
            records[i].future2_prate = prate
            records[i].future2_range = frange
        records[i].future3_prate = 0
        records[i].future3_range = 0  
        if i>3:
            prate = (records[i-4].close - records[i-1].close) / records[i-1].close
            frange = comm.getFutureRange(prate)
            records[i].future3_prate = prate
            records[i].future3_range = frange    
        #print records[i] 
     
    comm.fix_peak_trough(records,'peak_trough_5')

    save_stocks(stock_no,records)

    content1 = ','.join([k for k,v in records[0].items()]) + '\r'
    content1 =  content1 + '\r'.join([ ','.join([str(v) for k,v in r.items()]) for r in records])
    new_filepath1 = '%s/dailyh_add_csv/%s.csv' % (const_root_local,stock_no)    
    with open(new_filepath1, 'w') as file:
        file.write(content1)

    return records

def process2(stock_no):
    records = load_stocks(stock_no)
    count = len(records)    
    for i in range(0,count):
        records[i].ma5_trend_3 = comm.get_trend_2(records[i:i+3],'ma_5') if count-i>2 else 0                    
        records[i].ma5_trend_5 = comm.get_trend_2(records[i:i+5],'ma_5') if count-i>4 else 0
        # print '%s,%s,%s' %(records[i].ma5_trend_3,records[i].ma5_trend_5,records[i].future2_range)
    save_stocks(stock_no,records)
    return records      




  
from collections import Counter
def mapfn(stock_no,records):    
    rows = []
    total_count = len(records)
    trade_records = [r for r in records if r.volume>0]
    trade_count = len(trade_records)
    categories = dict(Counter(r[categoryField] for r in trade_records))

    rows.append(web.storage(fk='total',cv='',fv='',count=total_count,p=float(total_count)/trade_count))
    rows.append(web.storage(fk='trade',cv='',fv='',count=trade_count,p=float(trade_count)/trade_count))
    for k,v in categories.items():
        rows.append(web.storage(fk='category',cv=k,fv='',count=int(v),p=float(v)/trade_count))    
    for fk in featureFields:         
        cfvalues = dict(Counter('%s|%s|%s' % (fk,r[categoryField],r[fk]) for r in trade_records))
        for k,v in cfvalues.items():
            segs = k.split('|')
            rows.append(web.storage(fk=segs[0],cv=segs[1],fv=segs[2],count=int(v),p=float(v)/trade_count))
    
    content = '\r\n'.join(['%s,%s,%s,%s,%s' % (r.fk,r.cv,r.fv,r.count,r.p) for r in rows]) 
    save_sum_records(stock_no,content) 

def get_cv(k):
    segs = k.split('|')
    if len(segs)>2:
        return 'category|%s' % (k.split('|')[1])
    else:
        return 'trade' 

def reducefn():
    local_dir = "%s/dailyh_sum/"  % (const_root_local)   
    filenames = os.listdir(local_dir)
    
    d = {}   
    for f in filenames:
        stock_no = '.'.join(f.split('.')[0:2])
        sum_records = load_sum_records(stock_no) 
        for row in  sum_records:
            k='|'.join([r for r in (row.fk,row.cv,row.fv) if r])
            d[k] = d[k] + int(row.count) if k in d else int(row.count) 
      
    l = ['%s,%s,%s' % (k,v,float(v) / int(d[get_cv(k)])) for k,v in d.items()]
    content = '\r\n'.join(l)
    save_probability(content)



def gen_date_file(stock_no):
    records = load_stocks(stock_no)
    for r in records:
        new_filepath = '%s/dailyh_dates/%s.csv' % (const_root_local,r.trade_date) 
        content = ','.join([k for k,v in r.items()])  + '\r'   
        content = content + ','.join([str(v) for k,v in r.items()])         
        with open(new_filepath, 'w') as file: 
            file.write(content)



featureFieldsvvvvvvvv =('trend_3','trend_5','candle_sort','up_or_down','volume_level','jump_level','ma_5_10','ma_p_2','ma_p_3','ma_p_4','ma_p_5')
featureFieldssss =('trend_5','ma_p_5','ma_p_4','trend_3','candle_sort','ma_p_3','jump_level','volume_level','up_or_down','ma_5_10','ma_p_2',)
def compute_probability_one_stock(probabilities,stock_no):
    trade_records = load_stocks(stock_no)
    count = len(trade_records)
    print 'trade_date,c1,c2,c3,close,acp,future1_prate'
    for i in range(0,count): 
        c1 = 0.194520338846
        c2 = 0.604818399782
        c3 = 0.199873024089
        for fk in featureFieldssss: 
            fv = trade_records[i][fk]
            ps = [p for p in probabilities if p.fk==fk and p.fv==str(fv)]
            c1_p = [p.p for p in ps if p.cv=='1'][0] 
            c1 = c1 * float(c1_p)
            
            c2_p = [p.p for p in ps if p.cv=='2'][0] 
            c2 = c2 * float(c2_p)

            c3_p = [p.p for p in ps if p.cv=='3'][0] 
            c3 = c3 * float(c3_p)

            #print fk,fv,float(c1_p),float(c2_p)
        future1_range = trade_records[i]['future1_range'] if 'future1_range' in  trade_records[i] else 0
        future1_prate = trade_records[i]['future1_prate'] if 'future1_prate' in  trade_records[i] else 0

        print '%s,%s,%s,%s,%s,%s,%s' %(trade_records[i]['trade_date'],c1,c2,c3,trade_records[i]['close'],trade_records[i]['acp'],future1_prate)
        # print '---------------------'
        # if i==5:    
        #     break  

def test(stock_no):
    probabilities = load_probability()
    compute_probability_one_stock(probabilities,stock_no)

########################

def _____drop_multi_run(stock_no):
    ##须有最大进程数限制
    multiprocessing.Process(name=stock_no,target=process,args=(stock_no,)).start()     
    # worker_1 = multiprocessing.Process(name='worker 1',target=process,args=(stock_no,))  
    # worker_1.start()  

def process_callback():
    pass

def process(stock_no):
    process1(stock_no)
    records = process2(stock_no)
    mapfn(stock_no,records)
    print stock_no 

def run():
    local_dir = "%s/dailyh/"  % (const_root_local)   
    filenames = os.listdir(local_dir)
    mpPool = multiprocessing.Pool(processes=3) #<=机器的cpu数目
    for f in filenames:
        param = '.'.join(f.split('.')[0:2])
        mpPool.apply_async(process,(param,))        
    mpPool.close()
    mpPool.join()


if __name__ == "__main__":
    run()     
    reducefn()
    # gen_date_file('300104.sz')
    # process1('002639.sz')



    # reducefn()
    #load_stocks('000001.sz')
    
    # test('300104.sz')

    # rows = load_probability()
    # for r in rows:
    #     print r
    
    # xx = load_probability()
    # for x in xx:
    #     print x.fk,x.fv,x.cv,x.p,x.count

    #
    #
    
    