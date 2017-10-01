#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最新数据下载、解析
网易数据源
"""
import os
import sys
import datetime
import time
import json

import stock_meta
import common

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)
sys.path.append(home_dir + "/conf")
import conf


NEW_DATA_URL = 'http://api.money.126.net/data/feed/%s,money.api?callback=_ntes_quote_callback_%s'
# http://hq.sinajs.cn/list=sh600000,sh600004,sh600005,sh600006,sh600007,sh600008,sh600009,sh600010,sh600011,sh600012,sh600015,sh600016,sh600017,sh600018,sh600019,sh600020,sh600021,sh600022,sh600026,sh600027,sh600028,sh600029,sh600030,sh600031,sh600033,sh600035,sh600036,sh600037,sh600038,sh600039,sh600048,sh600050,sh600052,sh600053,sh600054,sh600055,sh600056,sh600057,sh600059,sh600060,sh600061,sh600062,sh600063,sh600064,sh600066,sh600067,sh600068,sh600069,sh600070,sh600071,sh600072,sh600073,sh600075,sh600076,sh600077,sh600078,sh600079,sh600080,sh600081,sh600082,sh600083,sh600084,sh600085,sh600086,sh600088,sh600089,sh600090,sh600091,sh600093,sh600094,sh600095,sh600096,sh600097,sh600098,sh600099,sh600100,sh600101,sh600103,sh600104,sh600105,sh600106,sh600107,sh600108,sh600109,sh600110,sh600111,sh600112,sh600113
# http://api.money.126.net/data/feed/0000001,0600012,1300184,1002902,0601857,0601600,0601398,0600028,0600019,0601318,0600030,0601939,0601088,0600900,1002024,0603136,0600593,0603869,1000888,1002159,money.api?callback=_ntes_quote_callback7451091

FIELDS_MAP = {
    # 'trade_date':'time',
    # 'trade_time':'time',
    # 'stock_exchange':'type',
    # 'create_time':'time',
    # 'update_time':'update'

    'stock_no': 'symbol',
    'open': 'open',
    'close': 'price',
    'high': 'high',
    'low': 'low',
    'last_close': 'yestclose',  # 前收盘价
    'turn_over': 'turnover',  # 换手率
    'CHG': 'updown',  # 涨跌额，收盘价-前收盘价
    'PCHG': 'percent',  # 涨跌幅，(收盘价-前收盘价)/前收盘价
    'vo_turn_over': 'volume',  # 成交量
    # 'va_turn_over': '',  # 成交金额
    # 't_cap':'', #总市值
    # 'm_cap':'', #流通市值

}

FIELDS_SORT = ("trade_date,trade_time,stock_no,stock_exchange,open,close,high,low,last_close,"
               "CHG,PCHG,turn_over,vo_turn_over,va_turn_over,t_cap,m_cap,create_time,update_time"
               )


def get_stock_no(stock):
    """转换exchange,公共方法？"""
    stock_no = stock['stock_no']
    if stock_no.startswith('6'):
        return '0' + stock_no
    else:
        return '1' + stock_no


def download(stocks, offset):
    """下载数据"""
    source_url = NEW_DATA_URL % (','.join(map(get_stock_no, stocks)), offset)
    file_local = "%s/%s.csv" % (conf.HISTORY_DATA_PATH, offset)

    if not (os.path.isfile(file_local) and os.path.getsize(file_local) != 0):
        os.system("wget -q '%s' -O %s" % (source_url, file_local))

    print source_url
    return load_local(file_local)
    # _ntes_quote_callback_3000(  )


def load_local(file_local):
    """转换"""
    json_str = ''
    with open(file_local) as f:
        content = f.read()
        json_str = content.split("(")[1].strip(");")

    stocks = json.loads(json_str, encoding="utf-8")
    return stocks


def convert_csv(stocks):
    for stock_no, trade in stocks.items():
        info = {}
        for k, v in FIELDS_MAP.items():
            info[k] = trade[v] if v in trade else 0

        info['stock_exchange'] = common.get_stock_exchange(info['stock_no'])

        # trade['time'] 2017/09/29 15:59:43
        dt_time = datetime.datetime.strptime(
            trade['time'], '%Y/%m/%d %H:%M:%S')
        dt_update = datetime.datetime.strptime(
            trade['update'], '%Y/%m/%d %H:%M:%S')

        info['trade_date'] = dt_time.strftime("%Y%m%d")
        info['trade_time'] = 1 if dt_time.strftime(
            "%p") == "PM" else 0  # pm1,am0
        info['create_time'] = int(time.mktime(dt_time.timetuple()))
        info['update_time'] = int(time.mktime(dt_update.timetuple()))

        li = []
        fields = FIELDS_SORT.split(',')
        for field in fields:
            li.append( str(info[field]) if field in info else '0' )

        print ','.join(li)


def main():
    """主函数"""
    stocks = list(stock_meta.load_all())
    len_stocks = len(stocks)

    offset = 0
    limit = 800
    while offset < len_stocks:
        #delete files ?
        stocks_trade = download(stocks[offset:offset + limit], offset)
        convert_csv(stocks_trade)
        offset = offset + limit  


if __name__ == "__main__":
    main()
