#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
历史数据下载 - 网易数据源
"""
import os
import sys
import time
import datetime
import requests
import logging

DOWNLOAD_FIELDS = "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
HISTORY_DATA_URL = 'http://quotes.money.163.com/service/chddata.html?code={code}&start={start}&end={end}&fields={fields}'


class HistoryData:
    def __init__(self, log, max_days=500):
        self.log = log
        self.max_days = max_days
        self.all_stocks_meta_file = "schema/dict/all_stocks_meta.txt"

    def get_cache_file(self, stock_no):
        return 'data/history_raw/%s.csv' % (stock_no)

    def download_single(self, stock_no, start=None):
        """下载数据"""
        cache_file = self.get_cache_file(stock_no) 
        if not start:
            start = (datetime.datetime.now() -
                     datetime.timedelta(self.max_days)).strftime("%Y%m%d")
        params = {"code": '0' + stock_no if stock_no.startswith('6') else '1' + stock_no,
                  "start": start,
                  "end": (datetime.datetime.now()+datetime.timedelta(1)).strftime("%Y%m%d"),
                  "fields": DOWNLOAD_FIELDS}
        source_url = HISTORY_DATA_URL.format(**params)

        resp = None
        for i in range(3):  # 失败最多重试3次
            try:
                resp = requests.get(url=source_url, timeout=0.5)
                self.log.info("download success,retry_times=%s,stock=%s,url=%s" %
                              (i, stock_no, source_url))
                break
            except: 
                if i == 2:  # 超过最大次数
                    self.log.warning("fail,retry_times=%s,stock=%s,url=%s" %
                                 (i, stock_no, source_url))
                    return
                else:
                    continue

        # 对返回结果再加工下,方便后续导入db，生成训练数据等
        new_lines = []
        lines = resp.text.split('\n')
        for lineNO, line in enumerate(lines):
            if lineNO == 0:
                continue
            line = line.replace('None', '0')
            fields = line.strip().split(',')
            if len(fields) < 2:
                break
            new_fields = []
            new_fields.append(fields[0].replace('-', ''))
            new_fields.append(fields[1].replace("'", ''))
            new_fields = new_fields + fields[3:]
            new_lines.append(",".join(new_fields))

        os.system("rm -f " + cache_file)
        with open(cache_file, 'w+') as f:
            f.write('\n'.join(new_lines))

    def load_all_stocks(self):
        li = []
        with open(self.all_stocks_meta_file, 'r') as f:
            # return [line.strip().split(',') for line in f]
            for line in f:
                fields = line.strip().split(',')
                if len(fields)>2 and fields[2]  :
                    continue 
                li.append(fields)
        return li 

    def download(self, topN=None):
        stocks = self.load_all_stocks()
        for i, stock in enumerate(stocks):
            if topN and i > topN:
                break
            self.download_single(stock[0])  # , stock[1]
            time.sleep(0.1)  # 0.1s 间隔


if __name__ == "__main__":
    log_file = "log/download_history.log"
    os.system("rm -f %s" % (log_file) )
    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format='%(levelname)s:%(asctime)s:%(lineno)d:%(funcName)s:%(message)s')
    obj = HistoryData(logging)
    obj.download()
    # lines = obj.load_all_stocks()
    # print(lines)
