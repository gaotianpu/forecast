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
import datafile

categoryField = 'future1_range'
featureFields =('trend_3','trend_5','candle_sort','up_or_down','volume_level','jump_level','ma_5_10','ma_p_2','ma_p_3','ma_p_4','ma_p_5','close_ma_5','close_ma_10','close_ma_20','close_ma_50','close_ma_100','close_ma_200')  

#################################

def process1(stock_no):  
    records = datafile.load_raw_records(stock_no)
    count = len(records)    
    # print 'trade_date,close,peak5,peak10'   

    for i in range(0,count):
        stock_no_infos = stock_no.split('.')
        records[i].stock_no = stock_no  #stock_no_infos[0]
        records[i].stock_pycode = stock_no_infos[1]

        #5日内波峰波谷
        records[i].peak_trough_5 = comm.get_peak_trough(records,count,i,3)
        ##records[i].peak_trough_10 = comm.get_peak_trough(records,count,i,5) #和5得出的结论基本吻合

        #100天内，最高值high，最低值low分布, 日期&具体的值
        rows = sorted(records[i:i+100], cmp=lambda x,y : cmp(x.close, y.close))  
        records[i].days100_low_close = rows[0].close
        records[i].days100_low_date = rows[0].trade_date 
        records[i].days100_high_close = rows[-1].close
        records[i].days100_high_date = rows[-1].trade_date   

        #成交量
        r10 = records[i:i+10]        
        l = [r.volume for r in r10]
        volume_avg_10 = reduce(lambda x, y: x + y, l) / len(l)
        volume_p = float(records[i].volume) / volume_avg_10  if volume_avg_10 else 0
        records[i].volume_avg_10 = volume_avg_10
        records[i].volume_level = comm.get_volume_level(volume_p)

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

        records[i].volume_cos_10 = comm.cos_dist( [r.volume for r in records[i:i+5]])

        #蜡烛图形态
        candles = comm.get_candle_2(records[i].open,records[i].close,records[i].high,records[i].low)
        records[i].range_1 = candles[0]
        records[i].range_2 = candles[1]
        records[i].range_3 = candles[2]
        records[i].candle_sort  = candles[4]
        records[i].up_or_down = 2 if candles[1]>0 else 1

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

        
        # current_record = records[i]
        # print '%s,%s,%s,%s' %(current_record.trade_date,current_record.close,records[i].peak_trough_5,records[i].peak_trough_10)
  
        
                   
        records[i].trend_3 = comm.get_trend(records[i:i+3]) if count-i>2 else 0                    
        records[i].trend_5 = comm.get_trend(records[i:i+5]) if count-i>4 else 0

        

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

        # comm.get_test(records,i)
        # datafile.gen_date_file(records[i])

    datafile.save_stocks(stock_no,records)
    return records

def process2(stock_no):
    records = datafile.load_stocks(stock_no)
    count = len(records)        
    for i in range(0,count):
        peaks = [r for r in records[i:] if r.peak_trough_5==2] #peak波峰         
        troughs = [r for r in records[i:] if r.peak_trough_5==1] #trough波谷
        if troughs and peaks:
           records[i].peak_trough_range = 'up' if troughs[0].trade_date > peaks[0].trade_date else 'down'
           records[i].zuli_price = peaks[0].high
           records[i].zhicheng_price = troughs[0].low
        else:
            records[i].peak_trough_range='--' 
            records[i].zuli_price = '-1'
            records[i].zhicheng_price = '-1'

        records[i].ma5_trend_3 = comm.get_trend_2(records[i:i+3],'ma_5') if count-i>2 else 0                    
        records[i].ma5_trend_5 = comm.get_trend_2(records[i:i+5],'ma_5') if count-i>4 else 0
        # print '%s,%s,%s' %(records[i].ma5_trend_3,records[i].ma5_trend_5,records[i].future2_range)
    datafile.save_stocks(stock_no,records)
    datafile.write_reports(stock_no,['trade_date','close','peak_trough_5','peak_trough_range','zuli_price','zhicheng_price'])
    return records  

##########################mapreduce#########################
  
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
    datafile.save_sum_records(stock_no,content) 

def get_cv(k):
    return 'category|%s' % (k.split('|')[1]) if len(k.split('|'))>2 else 'trade' 

def reducefn():
    local_dir = "%s/dailyh_sum/"  % (const_root_local)   
    filenames = os.listdir(local_dir)
    
    d = {}   
    for f in filenames:
        stock_no = '.'.join(f.split('.')[0:2])
        sum_records = datafile.load_sum_records(stock_no) 
        for row in  sum_records:
            k='|'.join([r for r in (row.fk,row.cv,row.fv) if r])
            d[k] = d[k] + int(row.count) if k in d else int(row.count) 
      
    l = ['%s,%s,%s' % (k,v,float(v) / int(d[get_cv(k)])) for k,v in d.items()]
    content = '\r\n'.join(l)
    datafile.save_probability(content)



featureFieldsvvvvvvvv =('trend_3','trend_5','candle_sort','up_or_down','volume_level','jump_level','ma_5_10','ma_p_2','ma_p_3','ma_p_4','ma_p_5')
featureFieldssss =('trend_5','ma_p_5','ma_p_4','trend_3','candle_sort','ma_p_3','jump_level','volume_level','up_or_down','ma_5_10','ma_p_2',)
def compute_probability_one_stock(probabilities,stock_no):
    trade_records = datafile.load_stocks(stock_no)
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
    probabilities = datafile.load_probability()
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
    print stock_no
    # process1(stock_no)
    records = process2(stock_no)
    mapfn(stock_no,records)

    # content1 = ','.join([k for k,v in records[0].items()]) + '\r'
    # content1 =  content1 + '\r'.join([ ','.join([str(v) for k,v in r.items()]) for r in records])

    # content1 = 'trade,close,volume\r'
    # content1 =  content1 + '\r'.join(['%s,%s,%s' %(r.trade_date,r.close,r.volume) for r in records])    
    # new_filepath1 = '%s/dailyh_add_csv/%s.csv' % (const_root_local,stock_no)    
    # with open(new_filepath1, 'w') as file:
    #     file.write(content1)

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

###############################

def test(trade_date):
    stocks = datafile.load_date(trade_date)
    stocks = [r for r in stocks if r.ma_5>r.ma_10 and r.trend_3==213 ]
    # for r in stocks:
    #     print r.ma_5,r.ma_10,r.trend_3
    # return 
    # rows = sorted(stocks, cmp=lambda x,y : cmp(x.trend_3, y.trend_3))
    
    rows = sorted(stocks, cmp=lambda x,y : cmp(x.days100_high_date, y.days100_high_date))
    print 'count:%s<br/>' % (len(rows))
    for r in rows:
        x = r.stock_no.split('.')
        r.pinyin = x[1] if x[1]!='ss' else 'sh'  
        r.no = x[0]
    #.roate{ -ms-transform:rotate(-90deg);-moz-transform:rotate(-90deg);-webkit-transform:rotate(-90deg);-o-transform:rotate(-90deg); } 
    print ''.join(['<a href="http://stockhtm.finance.qq.com/sstock/ggcx/%s.shtml" title="%s"><img src="http://image.sinajs.cn/newchart/daily/n/%s%s.gif" /></a> <img height="380" src="%s.png" /> <hr/>' %(r.no,r.days100_low_date,r.pinyin,r.no,r.stock_no )  for r in rows ] )
    #days100_high_date
    # for s in rows :
    #     print s.stock_no,s.days100_high_date

def test__2(stock_no):
    rows = datafile.load_raw_records(stock_no)
    l=[]
    for r in rows: #[0:200]:        
        l = l + comm.get_prices(r.high,r.low)
    price_counts = dict(Counter( l ))
    data = '\n'.join(['%s,%s' % (k,v) for k,v in price_counts.items()])   
    lfile = '%s/GaussianDistri/%s.csv' % (const_root_local,stock_no) 
    with open(lfile, 'w') as file: 
        file.write(data) 

def run_test_2():
    local_dir = "%s/dailyh/"  % (const_root_local)   
    filenames = os.listdir(local_dir)
    for f in filenames:
        print f        
        stock_no = '.'.join(f.split('.')[0:2])
        test__2(stock_no)   

import numpy 
import matplotlib.pyplot as plt
def draw_1(stock_no,current_price):  
    lfile = '%s/GaussianDistri/%s.csv' % (const_root_local,stock_no)
    data = numpy.loadtxt(lfile,delimiter=',')   

    current_position = (current_price - min(data[:,0]))/(max(data[:,0]) - min(data[:,0]))
    # return current_position
    
    #draw line
    max_y = 40 #max(data[:,1])
    point_x = current_price #data[:,0][list(data[:,1]).index(max_y)]  
    plt.plot([point_x,point_x],[0,max_y*1.1])

    plt.ylim([0.0,40.0])
    plt.plot(data[:,0],data[:,1],'ro')
    plt.xlabel('price:'+str(point_x))
    plt.ylabel('count:' + str(sum(data[:,1])) )
    img_file = '%s/GaussianDistriImg/%s.png' % (const_root_local,stock_no)  
    plt.savefig(img_file)
    plt.cla()
    # plt.clf()
    # plt.close()
    #plt.show()
    return current_position

def run_draw_1(trade_date):
    stocks = datafile.load_stocks_rawdata(trade_date)

    local_dir = "%s/GaussianDistri/"  % (const_root_local)   
    filenames = os.listdir(local_dir)
    l=[]
    for f in filenames: 
        print f
        f_segs = f.split('.') 
        stock_no = '.'.join(f_segs[0:2])
        try:
            close = 0 
            if f_segs[0] in stocks:
                close = stocks[ f_segs[0] ].close
            current_position = draw_1(stock_no,close) 
            l.append((stock_no,current_position))
        except Exception,e:
            print stock_no,e

    content  = '\n'.join(['%s,%s' %(r[0],r[1]) for r in l])
    lfile = '%s/current_position.csv' % (const_root_local)  
    with open(lfile, 'w') as file: 
        file.write(content) 

    l = sorted(l,cmp=lambda x,y : cmp(y[1], x[1]))    
    content  = '\n'.join(['<a href="http://stockhtm.finance.qq.com/sstock/ggcx/%s.shtml" ><img src="http://image.sinajs.cn/newchart/daily/n/%s%s.gif" /></a> <img src="%s.png" alt="%s" height="380" /> <hr/>' % (r[0].split('.')[0],r[0].split('.')[1].replace('ss','sh'),r[0].split('.')[0],r[0],r[1])  for r in l if r[1]>0.6 and r[1]<0.9 ])
    lfile = 'D:\\gaotp\stocks\\GaussianDistriImg\\cp_%s.html' % (trade_date)  
    with open(lfile, 'w') as file: 
        file.write(content) 

def tmp(stock_no):
    records = datafile.load_stocks(stock_no)
    for r in records:
        print r.trade_date,r.close,r.volume,r.volume_cos_10

def run_daily_report(trade_date):
    d_stocks = datafile.load_stocks_rawdata(trade_date)
    volumes = [v.volume for v in d_stocks.values()]
    closes = [v.volume*v.close for v in d_stocks.values()]
    opens = [v.volume*v.open for v in d_stocks.values()]
    up_count = len([v for v in d_stocks.values() if v.close>v.open])
    
    volume_avg = reduce(lambda x, y: x + y, volumes) / len(volumes)
    close_avg = reduce(lambda x, y: x + y, closes) / len(closes) / volume_avg
    open_avg = reduce(lambda x, y: x + y, opens) / len(opens) / volume_avg
        
    print trade_date,close_avg,volume_avg,float(up_count)/len(volumes),open_avg

    return web.storage(trade_date=trade_date,close=close_avg,volume=volume_avg,up_percent=float(up_count)/len(volumes),open=open_avg)

def run_daily_reports():
    path = "%s/daily_/"  % (const_root_local) 
    filenames = os.listdir(path)
    for f in filenames:
        run_daily_report(f.split('.')[0])

    # records = [run_daily_report(f.split('.')[0])  for f in filenames] #[-10:]
    # for r in records:
    #     print r

        

if __name__ == "__main__":
    # run()     
    # reducefn()
    # run_test_2()
    # run_draw_1('20140304')
    # run_daily_reports()
     
    
    # trade_date = '2014-02-26'  #datetime.datetime.now().strftime('%Y-%m-%d')    
    
    # datafile.gen_date_files(trade_date)
    # test(trade_date)
    
    # datafile.gen_date_file('300104.sz')
    # process1('300104.sz')
    # tmp('300104.sz')
    # process1('000002.sz')
    # process1('600616.ss')
    # process1('002276.sz')
    process2('300023.sz')
    
    # print datafile.load_stocks('000001.sz')



    # reducefn()
    #
    
    # test('300104.sz')

    # rows = datafile.load_probability()
    # for r in rows:
    #     print r
    
    # xx = datafile.load_probability()
    # for x in xx:
    #     print x.fk,x.fv,x.cv,x.p,x.count

    #
    #
    
    