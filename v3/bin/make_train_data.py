#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
根据未来n天的涨幅，决定分类标签，up-1，down-0
trade_date + stock_no, 未来一天，未来2天，未来3天的涨幅，生成label?
close=0的情况？
网易数据源
"""
import os
import sys
import numpy as np

import common

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)
sys.path.append(home_dir + "/conf")
import conf

log = common.init_logger()

# tail -10 ~/Documents/Github/forecast/v3/data/converted/600000.csv

# 日期0,股票代码1,收盘价2,最高价3,最低价4,开盘价5,前收盘6,涨跌额8,涨跌幅9,换手率10,成交量11,成交金额12,总市值13,流通市值14


def gen_future_row(data, index):
    #（未来5天的最高价 - 当前收盘价格)/当前收盘价格
    # min_price = data[0:15, get_index('low')].astype(np.float).min()
    if index == 0:
        return

    start_index = index - 5
    if start_index < 0:
        start_index = 0

    trade_date = data[index, 0]
    stock_no = data[index, 1]
    current_close = data[index, 2].astype(np.float)
    max_high = data[start_index:index, 3].astype(np.float).max()

    if current_close == 0 or max_high == 0:
        log.info("price0 trade_date=%s,stock_no=%s,current_close=%s,max_high=%s" % (
            trade_date, stock_no, current_close, max_high))
        return

    rate = (max_high - current_close) / current_close
    return [trade_date, stock_no, current_close, max_high, rate]


def gen_future(stock_no):
    csv_file = "%s/%s.csv" % (conf.HISTORY_CONVERTED_PATH, stock_no)
    target_file = "%s/%s.csv" % (conf.FUTURE_PATH, stock_no)

    trade_records = np.loadtxt(csv_file, dtype=np.str, delimiter=",")
    records_len = len(trade_records)

    lines = []
    for i, trade_record in enumerate(trade_records):
        l = gen_future_row(trade_records, i)
        if not l:
            continue

        lines.append(",".join([str(x) for x in l]) + "\r\n")

    with open(target_file, 'w') as f:
        f.writelines(lines)


if __name__ == "__main__":
    gen_future("600000")
