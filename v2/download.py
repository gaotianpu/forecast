#!/usr/bin/python
# -*- coding: utf-8 -*-

# 下载历史数据download_all_history()
# 下载最新数据 download_latest()
# 依赖all_stocks_list.txt文本，里面存放了股票编码，每行一个，例如sh600000\r\nsz000001,
# 需定期检查已退市股票，从该列表中移除  

# cat 2015-03-19.csv | grep '""'

#  
import os
import math
import datetime
import browser
import csv
import config


const_base_url="http://hq.sinajs.cn/list="
# http://hq.sinajs.cn/list=sh600000,sh600113,sz000001
# http://table.finance.yahoo.com/table.csv?s=000001.sz



def load_all_stocks():
    stocks = []
    with open(config.stocks_list_file,'rb') as f:
        lines = f.readlines()
        f.close()        
        for l in lines:            
            items = l.strip().strip().split(',')            
            stocks.append((items[0],items[0][2:]+'.'+items[0][:2].replace('sh','ss') ))                
    return stocks
        


def download_history(stock_no):    
    url = 'http://table.finance.yahoo.com/table.csv?s=%s' % (stock_no)     
    lfile = '%s%s.csv' %(config.history_data_dir,stock_no)
    # print url ,lfile     
    try:
        # if os.path.exists(lfile):
        #     os.remove(lfile)
        if not os.path.exists(lfile):
            print stock_no
            browser.downad_and_save(url,lfile)
    except Exception,e:
        print str(e) 


def download_all_history():
    stocks = load_all_stocks()
    for stock in stocks:        
        download_history(stock[1])

# note: http://blog.csdn.net/simon803/article/details/7784682
# 0：”大秦铁路”，股票名字；
# 1：”27.55″，今日开盘价；
# 2：”27.25″，昨日收盘价；
# 3：”26.91″，当前价格；
# 4：”27.55″，今日最高价；
# 5：”26.20″，今日最低价；
# 8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
# 9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
# 30：”2008-01-11″，日期；
# 31：”15:05:32″，时间；
def download_latest():
    latest_day = config.get_today()
    re_download = True

    pagesize = 88
    stocks = load_all_stocks()
    count = len(stocks)
    params = [s[0] for s in stocks]     
    pagecount = int(math.ceil(count/pagesize)) 
    
    dir_today = '%s%s/' %(config.daily_data_dir,latest_day)   

    print "download 下载文件"    
    for i in range(0,pagecount+1):
        print i
        url = const_base_url + ','.join(params[i*pagesize:(i+1)*pagesize])        
        lfile = '%s%s.csv' %(dir_today,i)
        if re_download:
            if not os.path.exists(dir_today):
                os.mkdir(dir_today) 
            if os.path.exists(lfile):
                os.remove(lfile) 
            try:
                browser.downad_and_save(url,lfile)
            except Exception,e:
                print str(e)

    print "merge 合并文件"
    #cat file1 file2.txt > all.csv, 可以采用linux shell方式处理，似乎更好些？
    lines = []
    for f in  os.listdir(dir_today): # range(0,pagecount+1):
        lfile = '%s%s' %(dir_today,f)
        with open(lfile,'r') as f:
            tlines = f.readlines()            
            for tl in tlines: 
                if  int(tl.split(',')[8])==0: continue                
                items = tl.split('=') 
                stock_no = items[0].split('_')[-1]
                stock_fields_str = items[1].replace('"','').replace(";","")
                x = stock_fields_str.split(',')
                
                #compute
                o = float(x[1]) #open
                lc = float(x[2]) #last close
                c = float(x[3]) #current price equal close
                h = float(x[4]) #high
                l = float(x[5]) #low 
                prate = (c-o)/o #计算涨幅
                jump = (o-lc)/lc #是否跳空 (今开 - 昨收) / 昨收
                maxp = (h-l)/o #蜡烛图的形态，high-low

                nline = ','.join([stock_no,x[1],x[2],x[3],x[4],x[5],x[8],x[9],x[30],x[31],str(prate),str(jump),str(maxp)])
                # nline = stock_no +','+ stock_fields_str          
                lines.append(nline)          
            f.close()

    current_hour = datetime.datetime.now().hour
    allfile = '%s%s.csv' %(config.daily_data_dir,latest_day) 
    if current_hour < 13 :
        allfile = '%s%s.am.csv' %(config.daily_data_dir,latest_day)
    with open(allfile,'w') as f:
        all_content = '\n'.join(lines)
        f.write(all_content)
        f.close()


if __name__ == "__main__" :  
    # load_all_stocks()
    # download_all_history()
    # download_history('600000.ss')
    download_latest()
    # merge_latest()




