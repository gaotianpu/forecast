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
import stock_meta

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)

sys.path.append(home_dir + "/conf")
import conf
import setting

fields = setting.FIELDS_SORT.split(',')


def get_next(rows, index, days=3, key='close'):
    """未来days天内表现，作为ml的分类label"""
    current = rows[index]
    current_val = float(current[key])

    ret = {}
    for day in range(1, days + 1):
        ret['next_%s_%s' % (day, key)] = None
        if index >= day:  # 未来1天
            next_row = rows[index - day]
            val = float(next_row[key])
            ret['next_%s_%s' % (day, key)] = val
            # 涨跌幅度
            if current_val:
                rate = (val - current_val) / current_val
                ret['next_%s_%s_rate' % (day, key)] = rate
            else:
                ret['next_%s_%s_rate' % (day, key)] = None

    return ret


def get_stat(rows, key):
    """获得 均值，标准差
    http://www.cnblogs.com/smallpi/p/4550361.html
    """
    ret = {}
    arr = np.array([float(row[key]) for row in rows])
    ret['last_%s_max' % key] = arr.max()
    ret['last_%s_min' % key] = arr.min()
    ret['last_%s_mean' % key] = arr.mean()
    ret['last_%s_std' % key] = arr.std()
    ret['last_%s_median' % key] = np.median(arr)  # .median()
    return ret


def get_last(rows, index, days=10):
    """过去days天内表现，ML的feather部分"""
    # 过去10个交易日的统计指标，均值，标准差，max(high)，min(low)，
    # open,close,high,low,成交量，换手率等，排除=0的情况
    # last_rows = rows[index:index+days]
    ret = {}

    last_rows = [row for row in rows[index:index + days]
                 if float(row['close']) > 0]
    if not last_rows:
        return ret

    # max,min
    ret['last_high_max'] = max([row['high'] for row in last_rows])
    ret['last_low_min'] = min([row['low'] for row in last_rows])

    ret_close = get_stat(last_rows, "close")
    ret_turn_over = get_stat(last_rows, "turn_over")
    ret_vo_turn_over = get_stat(last_rows, "vo_turn_over")

    ret = dict(ret.items() + ret_close.items() +
               ret_turn_over.items() + ret_vo_turn_over.items())

    current = rows[index]
    last_one = last_rows[-1]  # 最远的一个？

    # 再当前值的z-score ?

    ret['last_10_open'] = last_one['open']
    if last_one['open']:
        ret['last_10_rate'] = (float(current['open']) -
                               float(last_one['open'])) / float(last_one['open'])

    # ret['id'] = current['id']

    return ret


def rolling(rows, index):
    """处理单个stock"""
    current = rows[index] 

    # gen for label
    ret1 = get_next(rows, index, 3, "close")

    # gen for features
    ret2 = get_last(rows, index)

    ret = dict(ret1.items() + ret2.items())
    ret['id'] = current['id']

    return ret


def process_stock(stock_no, days):
    """处理单个stock"""
    csv_file = "%s/convert_%s.csv" % (conf.HISTORY_CONVERTED_PATH, stock_no)
    rows = common.load_csv(csv_file, fields)
    rows = list(rows)
    for i, row in enumerate(rows):
        print rolling(rows, i)


def main(days):
    """主函数，处理所有stocks"""
    stocks = stock_meta.load_all()
    for stock in stocks:
        process_stock(stock['stock_no'], days)
        # print stock


if __name__ == "__main__":
    # main(int(sys.argv[1]))
    process_stock('000001', 3)
