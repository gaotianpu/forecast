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
import json
import numpy as np

import common

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)
sys.path.append(home_dir + "/conf")
import conf

log = common.init_logger()

# tail -10 ~/Documents/Github/forecast/v3/data/converted/600000.csv

# 日期0,股票代码1,收盘价2,最高价3,最低价4,开盘价5,前收盘6,涨跌额8,涨跌幅9,换手率10,成交量11,成交金额12,总市值13,流通市值14

FUTURE_DAYS = 3
LAST_DAYS = 15


def gen_future_row(data, index):
    """target:(未来3天的收盘价 - 当前收盘价格)/当前收盘价格
    features: 过去15天，最低价、最高价、收盘均价(!=0)、收盘价标准差、
        过去3天，每天的收盘价
        归一化：都减去最低价，再除以最低价？
        # 价格：高、低、起、止、均值，波动范围
    # 成交量：z-score
    """
    future_index = index - FUTURE_DAYS
    last_start_index = index + LAST_DAYS

    if index < FUTURE_DAYS:
        return

    if last_start_index + 1 > len(data):
        return

    #
    future_data = data[future_index:index]
    last_data = data[index:last_start_index]

    # print last_data[0,0],last_data[-1,0]
    # return

    max_high = last_data[:, 3].astype(np.float).max()
    min_low = last_data[:, 4].astype(np.float).min()
    close_mean = last_data[:, 2].astype(np.float).mean()
    close_std = last_data[:, 2].astype(np.float).std()

    ptp = max_high - min_low
    wave_range = ptp / min_low  # 波动范围

    # last
    # 15天前close价
    start = last_data[-1]  # .astype(np.float)
    start_close = start[2].astype(np.float)
    start_range = (start_close - min_low) / ptp

    end = last_data[0]  # .astype(np.float)
    end_close = end[2].astype(np.float)
    end_range = (end_close - min_low) / ptp

    mean_range = (close_mean - min_low) / ptp

    # 成交量
    vol_mean = last_data[:, 11].astype(np.float).mean()
    vol_std = last_data[:, 11].astype(np.float).std()
    vol_current = last_data[0, 11].astype(np.float)
    vol_zscore = (vol_current - vol_mean) / vol_std

    # 预测
    current_close = end_close
    future_closes = future_data[0, 2].astype(np.float)
    future_rate = (future_closes - current_close) / future_closes

    # print last_data[0]
    results = {'last_start_date': last_data[-1, 0],
               'last_end_date': last_data[0, 0],
               'future_date': future_data[0, 0],
               'last_max_high': max_high,
               'last_min_low': min_low,
               'last_ptp': ptp,
               'last_wave_range': wave_range,
               'last_close_mean': close_mean,
               'last_close_std': close_std, 
                'last_start_close': start_close,
                'last_start_range': start_range,
                'last_end_close': end_close,
                'last_end_range': end_range,
                'last_mean_range': mean_range,
                'last_vol_zscore': vol_zscore
               }

    # print json.dumps(results)
    return last_data[0,0],future_rate,wave_range,mean_range,start_range,end_range,vol_zscore 
     


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
