#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import math
import da
import re

loger = init_log("stock_daily_import")

const_base_url="http://hq.sinajs.cn/list="

def get_local_file_name(index):
    return '%s/daily/%s_%s.txt' %(const_root_local,datetime.datetime.now().strftime('%Y%m%d'),index)

def run():
    stocks = da.stockbaseinfos.load_all_stocks()
    params = ['%s%s'%(s.pinyin2,s.stock_no)  for s in stocks]

    count = len(params)
    pagesize = 88
    pagecount = int(math.ceil(count/pagesize))
    print pagesize,count,pagecount
    rows = []
    for i in range(0,pagecount+1):
        url = const_base_url + ','.join(params[i*pagesize:(i+1)*pagesize])
        print i,url
        lfile = get_local_file_name(i)
        browser.downad_and_save(url,lfile)
        rows = rows + parse_data(lfile,i)

    ##insert into
    da.stockbaseinfos.import_daily_records('stock_daily_records',rows)


regex = re.compile("_[a-z]{2}([\d]+)=")
def parse_data(lfile,i):
    l=[]
    with open(lfile,'rb') as f:
        lines = f.readlines()
        f.close()
        for a in lines:
            fields = a.split(',')
            if(len(fields)<30):continue

            if fields[30] != datetime.datetime.now().strftime('%Y-%m-%d'):
                break

            stockno = regex.findall(a)
            if not stockno: break

            print {'stock_no':stockno[0],'date':fields[30],'open_price':fields[1],'high_price':fields[4],
                'low_price':fields[5],'close_price':fields[3],'volume':int(fields[8])/100,'amount': fields[9] ,
                'create_date':datetime.datetime.now()}
            l.append({'stock_no':stockno[0],'date':fields[30],'open_price':fields[1],'high_price':fields[4],
                'low_price':fields[5],'close_price':fields[3],'volume':int(fields[8])/100,'amount': fields[9] ,
                'create_date':datetime.datetime.now()})
    return l

if __name__ == '__main__':
    try:
        run()
    except Exception,e:
            loger.error( str(e) )
