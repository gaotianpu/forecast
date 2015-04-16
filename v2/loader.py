#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import numpy
import web
import config
import mailer

def load_stock_history(stock_no):    
    records = []
    lfile = '%s%s.csv' %(config.history_data_dir,stock_no)
    if not os.path.exists(lfile):
        return records
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close()
        for l in lines[1:] :
            items = l.strip().split(',')
            if items[5]=='000': continue
            #0.Date 1.Open  2.High  3.Low   4.Close 5.Volume  6.AdjClose
            r = web.storage(date=items[0],open=float(items[1]),high=float(items[2]),
                low=float(items[3]),close=float(items[4]),
                volume=int(items[5]),adjclose=float(items[6]),amount=0,last_close=0)                                        
            records.append(r)            
    return records


def load_daily_stocks(date):       
    lfile = '%s%s.csv' %(config.daily_data_dir,date)
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close()
        
    d = {} 
    for l in lines:
        items=l.strip().split(',')        
        r = web.storage(            
            open=float(items[1]),
            last_close=float(items[2]),
            close=float(items[3]),
            high=float(items[4]),
            low=float(items[5]),
            volume=float(items[6]),
            amount=float(items[7]),
            date=items[8],                
            time=items[9])   
        d[items[0]] = r  
        print r  
    return d


def load_daily_stocks_v2(date):       
    lfile = '%s%s.csv' %(config.daily_data_dir,date)
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close()

        
    li = []
    for l in lines:
        x=l.strip().split(',')         
        #compute
        o = float(x[1]) #open
        lc = float(x[2]) #last close
        c = float(x[3]) #current price equal close
        h = float(x[4]) #high
        l = float(x[5]) #low 
        prate = (c-o)/o #计算涨幅
        jump = (o-lc)/lc #是否跳空 (今开 - 昨收) / 昨收
        maxp = (h-l)/o #蜡烛图的形态，high-low

        r = web.storage(
            stock_no = x[0],            
            open= o,
            last_close= lc,
            close= c ,
            high= h,
            low= l,
            volume=int(x[6]),
            amount=float(x[7]),
            date=x[8],                
            time=x[9],
            jump= jump,
            prate = prate,
            maxp = prate)  

        li.append(r)

    tmp = [i for i in li if i.jump<0 and i.prate>0]
    tmp.sort(key=lambda x:x.jump)  #低开|低走|高走
    print len(tmp), tmp[0].date,tmp[0].time,
    c = '<br>'.join( ["%s,%s,%s" %(i.stock_no[2:],i.jump,i.prate)  for i in tmp[0:10]])
    mailer.send('d_%s_%s'%(tmp[0].date,tmp[0].time), c  )

    # print len(tmp)
    # for t in tmp:
    #     print t
    #     break
         
    

def merge_history_and_today(date):
    days = 100
    stocks = load_daily_stocks(date)
    for k,v in stocks.items():
        stock_no = k[2:]+'.'+k[:2].replace('sh','ss')         

        records = load_stock_history(stock_no)
        records.insert(0,v)  #去重？
        last_days = records[:days]
 
        #write to file
        lfile="%s%s.csv"%(config.latest_data_dir,stock_no)
        if os.path.exists(lfile):
            os.remove(lfile)

        content = '\n'.join( ["%s,%s,%s,%s,%s,%s,%s,%s"%(r.date,str(r.open), str(r.last_close),
            str(r.close),str(r.high),str(r.low),str(r.volume),str(r.amount)) for r in last_days]  )
        with open(lfile,'w') as f:
            f.write(content)
            f.close()

        break

def comput_ma(stock_no):
    compute = lambda records,days : '%.2f' % numpy.array([x.adjclose for x in records[i:i+days]]).mean() 
    cvolume = lambda records,days : '%.0f' % numpy.array([x.volume for x in records[i:i+days]]).mean() 
    
    l = []
    records = load_stock_history(stock_no)
    count  = len(records)
    for i in range(0,count): 
        r = records[i] 

        last_adj_close = '0'
        prate = 0
        jump = 0 
        is_raise = 0 
        if i<count-1:
            last_adj_close = records[i+1].adjclose
            prate = int((r.adjclose - last_adj_close)*1000/ last_adj_close) 
            if prate > 3:
                is_raise = 1 
            jump = int((r.open - last_adj_close)*1000/ last_adj_close)  

        ma5 = compute(records,5)
        ma10 = compute(records,10)   
        ma30 = compute(records,30)   
        ma60 =  compute(records,60) 
        ma120 = compute(records,120)  
        ma240 = compute(records,240)  

        v5 = cvolume(records,5)
        v10 = cvolume(records,10)   
        v30 = cvolume(records,30)   
        v60 =  cvolume(records,60) 
        v120 = cvolume(records,120)  
        v240 = cvolume(records,240)  
               
        l.append((r.date,str(is_raise),str(prate),str(jump),str(last_adj_close),ma5,ma10,ma30,ma60,ma120,ma240,v5,v10,v30,v60,v120,v240))

    #save to file
    lfile="%s%s.csv"%(config.history_ma_dir,stock_no)
    if os.path.exists(lfile):
        os.remove(lfile)
    content = '\n'.join(";".join(x) for x in l )
    with open(lfile,'w') as f:
        f.write(content)
        f.close()

def all_ma():
    stocks = download.load_all_stocks()
    for s in stocks:
        print s[1]
        comput_ma(s[1])                         
         

# 1：”27.55″，今日开盘价；
# 2：”27.25″，昨日收盘价；
# 3：”26.91″，当前价格；
# 4：”27.55″，今日最高价；
# 5：”26.20″，今日最低价；
# 6：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
# 7：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
# 8：”2008-01-11″，日期；
# 9：”15:05:32″，时间；

#a = today_close_price
#b = (today-n_day)_open_price
#经济学价格变化率：(a-b)/((a+b)/2)
def price_change_rate(stock_no,days):
    l = []
    records = load_stock_history(stock_no)
    count = len(records)
    # print count

    rates = []
    x = 300 if count>300+days else count-days
    for i in range(0,x):
        a =  records[i].close
        b =  records[i+days].open       
        prate = (a-b)/((a+b)/2)
        l.append( ';'.join([records[i].date,str(records[i].close),str(int(prate*1000))]) ) 
        rates.append(int(prate*1000))
    
    lfile="%s%s.csv"%(config.history_price_change_rate_dir,stock_no)
    content = '\n'.join(l)
    # with open(lfile,'w') as f:
    #     f.write(content)
    #     f.close()

    narray = numpy.array(rates) 
    mean = narray.mean()
    std = narray.std()
    count = len([r for r in rates if r > mean ])
    # len([r for r in ])
    print stock_no,mean,std,count,len(rates) #均值,标准差

    return rates
    # print float(len([i for i in l if i[1]>1]))/len(l)

def all_price_change_rate():
    stocks = download.load_all_stocks()
    for s in stocks:        
        rates = price_change_rate(s[1],3)
        # narray = numpy.array(rates) 
        # mean = narray.mean()
        # std = narray.std()
        # # len([r for r in ])
        # print s[1],mean,std #均值,标准差

#统计过去days天的成交量分布情况
def compute_Volume(stock_no,days):
    records = load_stock_history(stock_no)
    Volumes = [r.volume for r in records[:days]]
    narray = numpy.array(Volumes) 
    mean = narray.mean()
    std = narray.std()
    count = len([r for r in Volumes if r > mean ])
    # print s[1],mean,std #均值,标准差
    print stock_no,mean,std,count,len(Volumes) # narray.std() #均值,标准差 narray.var()方差,

import download
def all_volume():
    l = []
    stocks = download.load_all_stocks()
    for s in stocks:
        print s[1]
        item = compute_Volume(s[1],300)



    
if __name__ == "__main__" :      
    # load_stock_history('600000.ss')
    load_daily_stocks_v2('2015-04-13')    
    # price_change_rate('600000.ss',3)
    # all_price_change_rate()
    # merge_history_and_today('2015-04-07')
    # compute_Volume('600000.ss',300)   
    # all_volume()
    # comput_ma('600000.ss')
    # all_ma()

