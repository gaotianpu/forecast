#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
历史数据 下载、解析、转换、导入
网易数据源
"""
import os
import sys
import datetime
import time
import pandas as pd

import stock_meta
# import common

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)
sys.path.append(home_dir + "/conf")
import conf
import setting

# 历史数据源
HISTORY_DATA_URL = 'http://quotes.money.163.com/service/chddata.html?code={code}&start={start}&end={end}&fields={fields}'
# http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html?year=2017&season=3
# http://quotes.money.163.com/service/chddata.html?code=0000001&start=19901219&end=20170929&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER
# http://quotes.money.163.com/service/chddata.html?code=1399001&start=19910403&end=20170929&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER
# http://quotes.money.163.com/service/chddata.html?code=1300184&start=20110222&end=20170929&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
# http://quotes.money.163.com/service/chddata.html?code=0600012&start=20030107&end=20171001&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
# http://quotes.money.163.com/service/chddata.html?code=1002159&start=20070817&end=20171001&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP

DOWNLOAD_FIELDS = "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"

DAYS = 365

def get_history_file(stock_no):
    return "%s/%s.csv" % (conf.HISTORY_DATA_PATH, stock_no)

def get_convert_file(stock_no):
    return "%s/%s.csv" % (conf.HISTORY_CONVERTED_PATH, stock_no)

def download(stock_no,start):
    """下载数据"""
    # stock_no = stock_info['stock_no']
    # start = stock_info['start']

    file_local = get_history_file(stock_no)

    if not start:
        start = (datetime.datetime.now() -
                 datetime.timedelta(DAYS)).strftime("%Y%m%d")
    params = {"code": '0' + stock_no if stock_no.startswith('6') else '1' + stock_no,
              "start": start,
              "end": datetime.datetime.now().strftime("%Y%m%d"),
              "fields": DOWNLOAD_FIELDS}
    source_url = HISTORY_DATA_URL.format(**params)

    # if not (os.path.isfile(file_local) and os.path.getsize(file_local) != 0):
    os.system("wget -q '%s' -O %s" % (source_url, file_local))  
    # stock_info['source_url'] = source_url
    # stock_info['file_local'] = file_local
    # return stock_info

#日期0,股票代码1,名称2,收盘价3,最高价4,最低价5,开盘价6,前收盘7,涨跌额8,涨跌幅9,换手率10,成交量11,成交金额12,总市值13,流通市值14
#2017-12-28,'000001,平安银行,13.21,13.46,13.02,13.28,13.29,-0.08,-0.602,0.918,155303047,2052944539.14,2.26821134145e+11,2.23486875614e+11
def convert(stock_no):
    raw_file = get_history_file(stock_no)
    target_file = get_convert_file(stock_no)
    
    lines = []
    with open(raw_file) as f: 
        for i,line in enumerate(f):
            if i<1: continue 
            l=[]
            x=line.strip().split(',')
            
            if x[3]=='0.0':continue
            l.append(x[0].replace('-',''))
            l.append(x[1].replace("'",'1'))
            l.extend(x[3:]) 
            lines.append(",".join(l)+"\r\n") 

    with open(target_file, 'w') as f:
        f.writelines(lines)  

if __name__ == "__main__":
    # main()
    convert('300706')
    # stock={'stock_no': '300706', 'start': '20170926'}
    # download_one(stock)
