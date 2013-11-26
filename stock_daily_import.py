#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import math
import da
import re
import datetime
import browser
from decimal import *
from config import const_root_local,init_log
import comm


loger = init_log("stock_daily_import")

const_base_url="http://hq.sinajs.cn/list="

def get_local_file_name(index):
    return '%s/daily/%s_%s.txt' %(const_root_local,datetime.datetime.now().strftime('%Y%m%d'),index)

regex = re.compile("_[a-z]{2}([\d]+)=")
def parse_data_and_import_to_db(lfile,i):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    pkids = da.dailyrecords.load_pkids(today)

    with open(lfile,'rb') as f:
        lines = f.readlines()
        f.close()

    rows=[]
    for a in lines:
        fields = a.split(',')
        if(len(fields)<30):continue

        if fields[30] != today:
            break

        stockno = regex.findall(a)
        if not stockno: break

        #if exist,update,
        raise_drop = Decimal(fields[3]) - Decimal(fields[2])
        raise_drop_rate = raise_drop / Decimal(fields[1]) * 100 if Decimal(fields[1]) != 0 else 0

        #
        stock_name = fields[0].split('"')[1].decode('gbk').encode("utf-8")
        da.stockbaseinfos.update(stockno[0],stock_name,fields[1],fields[3],fields[4],fields[5],int(fields[8])/100,fields[9],fields[30])

        if pkids and stockno[0] in pkids.keys():
            da.dailyrecords.update(pkids[stockno[0]],open_price=fields[1],high_price=fields[4],
            low_price=fields[5],close_price=fields[3],volume=int(fields[8])/100,amount=fields[9],
            adj_close=fields[2],
            raise_drop = raise_drop,
            raise_drop_rate = raise_drop_rate ,
            last_update=datetime.datetime.now())
            continue

        #else insert
        rows.append({'stock_no':stockno[0],'date':fields[30],'open_price':fields[1],'high_price':fields[4],
            'low_price':fields[5],'close_price':fields[3],'volume':int(fields[8])/100,'amount': fields[9] ,
            'adj_close':fields[2],
            'raise_drop':raise_drop,
            'raise_drop_rate':raise_drop_rate,
            'create_date':datetime.datetime.now()})

    ##insert into
    da.stockbaseinfos.import_daily_records('stock_daily_records',rows)

def import_stockbaseinfos(today,rows):
    #stock_base_infos
    for r in rows:
        #update(stockno,stockname,openp,close,high,low,volumn,amount,trade_day):
        da.stockbaseinfos.update(r.stock_no,open_price=r.open_price,high_price=r.high_price,
            low_price = r.low_price,close_price=r.close_price,volume=r.volume,amount=r.amount,
            adj_close = r.adj_close,
            raise_drop = r.raise_drop,
            raise_drop_rate = r.raise_drop_rate ,
            last_update=datetime.datetime.now())
    #stock_daily_records

def run():
    if not comm.is_trade_day(): return
    today = datetime.datetime.now()

    stocks = da.stockbaseinfos.load_all_stocks()
    params = ['%s%s'%(s.pinyin2,s.stock_no)  for s in stocks]

    count = len(params)
    pagesize = 88
    pagecount = int(math.ceil(count/pagesize))
    print pagesize,count,pagecount

    for i in range(0,pagecount+1):
        url = const_base_url + ','.join(params[i*pagesize:(i+1)*pagesize])
        print i,url
        lfile = get_local_file_name(i)
        browser.downad_and_save(url,lfile)
        #rows = comm.parse_daily_data(lfile)

        parse_data_and_import_to_db(lfile,i)

    da.dailyrecords.update_marketcode(today)
    da.dailyrecords.import_date_sums(today.strftime('%Y%m%d'))

if __name__ == '__main__':
    run()

    import max_min_date
    max_min_date.run()

    import last_3_5
    last_3_5.run()







