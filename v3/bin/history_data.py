#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
历史数据 下载、解析
网易数据源
"""
import os
import sys
import datetime
import time
home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)
sys.path.append(home_dir + "/conf")
import conf
import stock_meta
import common

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

    if not (os.path.isfile(file_local) and os.path.getsize(file_local) != 0):
        os.system("wget '%s' -O %s" % (source_url, file_local))

    stock_info['source_url'] = source_url
    stock_info['file_local'] = file_local
    return stock_info


def load_all(file_path):
    """读取本地数据 公共方法？"""
    with open(file_path) as f:
        # rows = csv.DictReader(f)
        for i, line in enumerate(f):
            if i != 0:
                yield line.strip().split(',')





def convert_item(row):
    """每行的数据转换"""
    li = []
    li.append(row[0].replace('-', ''))  # trade_date
    li.append(1)  # trade_time
    stock_no = row[1].replace("'", '')
    stock_exchange = common.get_stock_exchange(stock_no)

    li.append(stock_no)  # stock_no
    li.append(stock_exchange)  # stock_no

    li.extend(row[3:])
    li.append(int(time.time()))  # create_time
    li.append(int(time.time()))  # update_time

    print ','.join([str(x) for x in li])

    # return ','.join([str(x) for x in li])+'\n'


def convert(stock_info):
    """ 格式转换为db需要的表
    {'stock_no': '300706', 
    'start': '20170926', 
    'file_local': '/Users/baidu/Documents/Github/forecast/v3/conf/../data/history/300706.csv', 
    'source_url': ' """ 
    rows = load_all(stock_info['file_local'])
    lines = map(convert_item, rows) 

    file_local = "%s/convert_%s.csv" % (conf.HISTORY_DATA_PATH,
                                        stock_info['stock_no'])
    # with open(file_local, 'w') as f:
    #     f.writelines(lines)


def main():
    """主函数"""
    stocks = stock_meta.load_all()
    map(convert, map(download, stocks))


if __name__ == "__main__":
    main()
    
    #  convert(
    #     {'file_local': '/Users/baidu/Documents/Github/forecast/v3/data/history/300706.csv',
    #      'stock_no': '300706'})
    
    # download('300184')
