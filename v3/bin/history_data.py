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

import stock_meta
import common

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


def download(stock_info):
    """下载数据"""
    stock_no = stock_info['stock_no']
    start = stock_info['start']

    file_local = "%s/%s.csv" % (conf.HISTORY_DATA_PATH, stock_no)

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
        # sys.stderr.write(stock_no + '\n')
    print source_url,file_local
    stock_info['source_url'] = source_url
    stock_info['file_local'] = file_local
    return stock_info


fields="id,trade_date,trade_time,stock_exchange,stock_no,close,high,low,open,last_close,CHG,PCHG,turn_over,vo_turn_over,va_turn_over,t_cap,m_cap,create_time,update_time"
def convert_item(row):
    """每行的数据转换"""
    trade_date = row[0].replace('-', '')
    stock_no = row[1].replace("'", '')

    info = {'id': trade_date + "1" + stock_no,
            'trade_date': trade_date,
            'trade_time': 1,
            'stock_exchange': common.get_stock_exchange(stock_no),
            'stock_no': stock_no,
            'close': row[3],  # 当前价格
            'high': row[4],
            'low': row[5],
            'open': row[6],
            'last_close': row[7],  # 前收盘价
            'CHG': row[8],  # 涨跌额，收盘价-前收盘价
            'PCHG': row[9],  # 涨跌幅，(收盘价-前收盘价)/前收盘价
            'turn_over': row[10],  # 换手率
            'vo_turn_over': row[11],  # 成交量
            'va_turn_over': row[12],  # 成交金额
            't_cap': row[13],  # 总市值
            'm_cap': row[14],  # 流通市值
            'create_time': int(time.time()),
            'update_time': int(time.time())
            }

    li = []
    fields = setting.FIELDS_SORT.split(',')
    for field in fields:
        li.append(str(info[field]) if field in info else '0') 
        
    return ','.join(li) + '\n'


def convert(stock_info):
    """ 格式转换为db需要的表
    {'stock_no': '300706', 
    'start': '20170926', 
    'file_local': '/Users/baidu/Documents/Github/forecast/v3/conf/../data/history/300706.csv', 
    'source_url': ' """
    file_local = "%s/%s.csv" % (conf.HISTORY_CONVERTED_PATH,
                                stock_info['stock_no'])

    if os.path.isfile(file_local) and os.path.getsize(file_local) != 0:
        return

    rows = common.load_all(stock_info['file_local'])
    lines = []
    try:
        lines = map(convert_item, rows)
    except Exception as ex:
        os.system("rm -f " + stock_info['file_local'])
        print stock_info
        print ex
        return

    with open(file_local, 'w') as f:
        f.writelines(lines)
    stock_info['convert_file'] = file_local

    return stock_info


def download_one(stock):
    download(stock)
    convert(stock)

def main():
    """主函数"""
    stocks = stock_meta.load_all()
    for stock in stocks:
        print stock
        download_one(stock) 


if __name__ == "__main__":
    main()
    # stock={'stock_no': '300706', 'start': '20170926'}
    # download_one(stock)
