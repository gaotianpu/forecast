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
import config


const_base_url="http://hq.sinajs.cn/list="
# http://hq.sinajs.cn/list=sh600000,sh600113,sz000001
# http://table.finance.yahoo.com/table.csv?s=000001.sz

def get_today():
    today = datetime.datetime.now()
    trade_date = today.strftime('%Y-%m-%d')
    return trade_date

def load_all_stocks():
    stocks = []
    with open(config.stocks_list_file,'rb') as f:
        lines = f.readlines()
        stocks = [(s.strip(),s[2:].strip()+'.'+s[:2].replace('sh','ss'))  for s in lines]
        f.close()
    return stocks
        


def download_history(stock_no):    
    url = 'http://table.finance.yahoo.com/table.csv?s=%s' % (stock_no)     
    lfile = '%s%s.csv' %(config.history_data_dir,stock_no)
    # print url ,lfile
    if os.path.exists(lfile):
        os.remove(lfile) 
    try:
        browser.downad_and_save(url,lfile)
    except Exception,e:
        print str(e) 


def download_latest():
    pagesize = 88
    stocks = load_all_stocks()
    count = len(stocks)
    params = [s[0] for s in stocks]     
    pagecount = int(math.ceil(count/pagesize))    

    print "download 下载文件"
    dir_today = '%sdaily/%s/' %(config.local_root_dir,get_today())
    for i in range(0,pagecount+1):
        url = const_base_url + ','.join(params[i*pagesize:(i+1)*pagesize])        
        lfile = '%s%s.csv' %(dir_today,i)
        if not os.path.exists(dir_today):
            os.mkdir(dir_today)  
        try:
            browser.downad_and_save(url,lfile)
        except Exception,e:
            print str(e)
    
    print "merge 合并文件"
    #cat file1 file2.txt > all.csv, 可以采用linux shell方式处理，似乎更好些？
    lines = []
    for i in range(0,pagecount+1):
        lfile = '%s%s.csv' %(dir_today,i)
        with open(lfile,'r') as f:
            tlines = f.readlines()            
            lines = lines + [tl.split('=')[1].replace('"','').replace(";","") for tl in tlines]            
            f.close()

    allfile = '%sdaily/%s.csv' %(config.local_root_dir,get_today())
    with open(allfile,'w') as f:
        all_content = ''.join(lines)
        f.write(all_content)
        f.close()

        

def download_all_history():
    stocks = load_all_stocks()
    for stock in stocks:
        download_history(stock[1])


if __name__ == "__main__" :
    # download_all_history()
    download_history('600000.ss')
    # download_latest()




