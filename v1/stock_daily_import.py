#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import math
import da
import re
import datetime
from util import browser
from decimal import *
from config import const_root_local,init_log
import comm


loger = init_log("stock_daily_import")

const_base_url="http://hq.sinajs.cn/list="
# http://hq.sinajs.cn/list=sh600000,sh600004,sh600005,sh600006,sh600007,sh600008,sh600009,sh600010,sh600011,sh600012,sh600015,sh600016,sh600017,sh600018,sh600019,sh600020,sh600021,sh600022,sh600026,sh600027,sh600028,sh600029,sh600030,sh600031,sh600033,sh600035,sh600036,sh600037,sh600038,sh600039,sh600048,sh600050,sh600052,sh600053,sh600054,sh600055,sh600056,sh600057,sh600059,sh600060,sh600061,sh600062,sh600063,sh600064,sh600066,sh600067,sh600068,sh600069,sh600070,sh600071,sh600072,sh600073,sh600075,sh600076,sh600077,sh600078,sh600079,sh600080,sh600081,sh600082,sh600083,sh600084,sh600085,sh600086,sh600088,sh600089,sh600090,sh600091,sh600093,sh600094,sh600095,sh600096,sh600097,sh600098,sh600099,sh600100,sh600101,sh600103,sh600104,sh600105,sh600106,sh600107,sh600108,sh600109,sh600110,sh600111,sh600112,sh600113


def get_local_file_name(index):
    day = datetime.datetime.now().strftime('%Y%m%d')
    return '%s/daily/%s_%s.txt' %(const_root_local,day,index) 

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
        #da.stockbaseinfos.update(stockno[0],stock_name,fields[1],fields[3],fields[4],fields[5],int(fields[8])/100,fields[9],fields[30])
        stock_market_no = comm.get_market_codes(stockno[0])['plate']
        if pkids and stockno[0] in pkids.keys():
            da.dailyrecords.update(pkids[stockno[0]],open_price=fields[1],high_price=fields[4],
            low_price=fields[5],close_price=fields[3],volume=int(fields[8])/100,amount=fields[9],
            adj_close=fields[2],
            raise_drop = raise_drop,
            raise_drop_rate = raise_drop_rate ,
            stock_market_no = stock_market_no,
            last_update=datetime.datetime.now())
            continue

        #else insert
        rows.append({'stock_no':stockno[0],'date':fields[30],'open_price':fields[1],'high_price':fields[4],
            'low_price':fields[5],'close_price':fields[3],'volume':int(fields[8])/100,'amount': fields[9] ,
            'adj_close':fields[2],
            'raise_drop':raise_drop,
            'raise_drop_rate':raise_drop_rate,
            'stock_market_no' : stock_market_no,
            'create_date':datetime.datetime.now()})

    ##insert into
    da.stockbaseinfos.import_daily_records('stock_daily_records',rows)

import file_history_process 
def run():
    if not comm.is_trade_day(): return

    stocks = da.stockbaseinfos.load_all_stocks()
    params = ['%s%s'%(s.pinyin2,s.stock_no)  for s in stocks]

    count = len(params)
    pagesize = 88
    pagecount = int(math.ceil(count/pagesize))
    print pagesize,count,pagecount

    for i in range(0,pagecount+1):
        url = const_base_url + ','.join(params[i*pagesize:(i+1)*pagesize])
        print i,url
        break 

        lfile = get_local_file_name(i)
        browser.downad_and_save(url,lfile)
        rows = comm.parse_daily_data(lfile)
        
        try:
            for r in rows:
                file_history_process.add_new_record(r)
            pass
        except Exception,ex:
            loger.error('stockdaily_cud import_rows ' + str(ex))
        
        try:
            da.stockdaily_cud.import_rows(rows)            
        except Exception,ex:
            loger.error('stockdaily_cud import_rows ' + str(ex))

        #update stockbaseinfos
        da.stockbaseinfos.import_rows(rows)
        parse_data_and_import_to_db(lfile,i)

import os
def merge_daily_data(trade_date):
    path = '%s/daily/' %(const_root_local) 
    filenames = os.listdir(path)
    rows = []
    for f in filenames:           
        if not f.startswith(trade_date):
            continue         
        rows = rows + comm.parse_daily_data(path+f)

    content = '\n'.join(['%s,%s,%s,%s,%s,%s,%s' %(r.market_codes.pinyin, r.stock_no,r.open_price,r.close_price,r.high_price,r.low_price,r.volume) for r in rows if r.volume>0])
    lfile =  '%s/daily_/%s.csv' %(const_root_local,trade_date) 
    with open(lfile, 'w') as file: 
        file.write(content)      

def run_release():
    run()

    today = datetime.datetime.now()
    trade_date = today.strftime('%Y%m%d')

    try:
        merge_daily_data(trade_date)
    except Exception,ex:
        loger.error('stockdaily_cud update_last_high_low' + str(ex))
    
    #lowprice_3_5
    try:            
        da.stockdaily_cud.update_last_high_low()
    except Exception,ex:
        loger.error('stockdaily_cud update_last_high_low' + str(ex))
    
    try:
        import lowprice_3_5            
        lowprice_3_5.run()
    except Exception,ex:
        loger.error('lowprice_3_5 run' + str(ex))

    
    try:
        #da.dailyrecords.update_marketcode(today)
        da.dailyrecords.import_date_sums(today.strftime('%Y%m%d'))
    except Exception,ex:
        loger.error('import_date_sums' + str(ex))

    try:    
        import max_min_date
        max_min_date.run()
    except Exception,ex:
        loger.error('max_min_date' + str(ex))

    try:        
        import last_3_5
        last_3_5.run()
    except Exception,ex:
        loger.error('last_3_5' + str(ex))

    try:        
        da.dailyrecords.remove_daily_records(datetime.datetime.now().strftime("%y-%m-%d"))
    except Exception,ex:
        loger.error('last_3_5' + str(ex))

    try:    
        import daily_sum_report
        daily_sum_report.run()
    except Exception,ex:
        loger.error('daily_sum_report' + str(ex))

    try:    
        import gua
        gua.run()
    except Exception,ex:
        loger.error('gua' + str(ex))

    try:    
        import cyb
        cyb.run_chart()
    except Exception,ex:
        loger.error('cyb.run_chart' + str(ex))

def tmp():
    filenames = os.listdir("D:\\gaotp\\stocks\\daily\\")
    l = [f.split('_')[0] for f in filenames]
    trade_dates = list(set(l))
    for date in  trade_dates:
        merge_daily_data(date)
    

if __name__ == '__main__':
    run()
    # run_release()
    # tmp()
    # merge_daily_data('20140224')
    # merge_daily_data('20140225')
    # merge_daily_data('20140226')
    # merge_daily_data('20140227')
    # merge_daily_data('20140228')

    
     

    # run()
    

    #
    #run_release()
    #da.dailyrecords.remove_daily_records('2013-12-10')

    #da.dailyrecords.update_marketcode(datetime.datetime.now())











