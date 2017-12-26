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
import traceback

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

def main(line):
    """main"""
    print line.split(',') 


if __name__ == "__main__":
    main(sys.argv[1])