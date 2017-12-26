#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用numpy计算最大值，最小值，均值，标准差，z-score等
"""
import os
import sys
import numpy as np

import common
import stock_meta

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)

sys.path.append(home_dir + "/conf")
import conf
import setting


def get_index(field_name):
    fields = setting.FIELDS_SORT.split(',')
    return fields.index(field_name)


def process(stock_no):
    # https://www.cnblogs.com/harvey888/p/5717098.html
    csv_file = "%s/convert_%s.csv" % (conf.HISTORY_CONVERTED_PATH, stock_no)
    # print csv_file
    data = np.loadtxt(csv_file, dtype=np.str, delimiter=",")

    # print get_index('open'),get_index('close'),get_index('high'),get_index('low'),get_index('vo_turn_over')
    # print data[0:15]
    # print get_index('low')
    # print data[data[:,8]>0]

    a = data[:, get_index('low')].astype(np.float)
    data = data[np.where(a > 0.0)][0:15]

    min_price = data[0:15, get_index('low')].astype(np.float).min()
    # print min_price
    # return

    # 极差（PTP）、方差（Variance）、标准差（STD）、变异系数（CV）
    max_price = data[0:15, get_index('high')].astype(np.float).max()
    min_price = data[0:15, get_index('low')].astype(np.float).min()
    ptp_price = max_price - min_price
    mean_price = data[0:15, get_index('close')].astype(np.float).mean()
    if not mean_price:
        return

    std_price = data[0:15, get_index('close')].astype(np.float).std()
    cv_price = std_price / mean_price
    zscore_price = (data[0, get_index('close')].astype(
        np.float) - mean_price) / std_price
    # print max_price,min_price,mean_price,std_price,cv_price,zscore_price

    vo = data[0:15, get_index('vo_turn_over')].astype(np.float)
    # print vo[0]
    trade_date = data[0, 1]

    print ','.join([str(i) for i in ['stock_' + stock_no, trade_date, max_price, min_price, mean_price, std_price, cv_price, zscore_price, vo.max(), vo.min(), vo.ptp(), vo.mean(), vo.std(), vo.std() / vo.mean(), (vo[0] - vo.mean()) / vo.std()]])


def process_record(data, index, days=3):
    records_len = len(data)
    if (index + days ) >= records_len :
        return 

    result = data[index:index + days]
    if len(result) < days:
        return
    close = result[:, get_index('close')].astype(np.float)
    if close.min() == 0.0:
        return 

    current = data[index + days]
    # print (close[0] - close[-1])/close[-1]
    print "\t".join([str(i) for i in (current[1], current[3], days, close[-1], close[0], (close[0] - close[-1]) / close[-1])])
    # print close
    # print result[0]
    # print result[-1]


def process_stock(stock_no):
    csv_file = "%s/convert_%s.csv" % (conf.HISTORY_CONVERTED_PATH, stock_no)
    # print csv_file
    trade_records = np.loadtxt(csv_file, dtype=np.str, delimiter=",")
    records_len = len(trade_records)
    for i, trade_record in enumerate(trade_records): 
        process_record(trade_records, i, 3)


def main():
    stocks = stock_meta.load_all()
    # print "stock_no,trade_date,max_price,min_price,mean_price,std_price,cv_price,zscore_price,vo_max,vo_min,vo_ptp,vo_mean,vo_std,vo_cv,vo_zscore"
    for stock in stocks:
        # print stock
        try:
            process_stock(stock['stock_no'])
        except Exception as e:
            print e

def init_log():
    """初始化日志"""  
    log_file = '%s/log/push_qingyuedu' % (conf.DATA_ROOT)
    log_file_handler = TimedRotatingFileHandler(
        filename=log_file, when="midnight", interval=1, backupCount=20)
    log_file_handler.suffix = "%Y%m%d.log"
    log_file_handler.extMatch = re.compile(r"^\d{8}.log$")
    log_format = '%(filename)s %(module)s %(funcName)s \
%(lineno)d %(levelname)s %(asctime)s %(message)s'
    formatter = logging.Formatter(log_format)
    log_file_handler.setFormatter(formatter)
    log_obj = logging.getLogger('')
    log_obj.addHandler(log_file_handler)
    log_obj.setLevel(conf.log_level)
    return log_obj

log = log_obj
if __name__ == "__main__":
    process_stock("600000")
    # main()
