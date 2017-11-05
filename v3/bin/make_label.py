#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
根据未来n天的涨幅，决定分类标签，up-1，down-0
trade_date + stock_no, 未来一天，未来2天，未来3天的涨幅，生成label?

网易数据源
"""
import os
import sys
import common
import stock_meta

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)

sys.path.append(home_dir + "/conf")
import conf


def process_trade_day(li, i, days, key):
    if (i - days) < 0:
        return None

    current = li[i]
    if current[key] == '0.0':
        return None 

    forcast = li[i - days]
    CHG = round(float(forcast[key]) - float(current[key]), 2) #涨跌额
    PCHG = round(100 * CHG / float(current[key]), 1) #涨跌幅

    # print forcast[0], current[key], forcast[key]
    ret = (current[0],current[1], current[3],forcast[1],CHG, PCHG)
    print ','.join( str(x) for x in ret )
    
    # return (current[0], current[2], CHG, PCHG)


def process_stock(stock_no,days):
    lines = common.load_all("%s/convert_%s.csv" % (conf.HISTORY_DATA_PATH,stock_no))
    lines = list(lines)
    count = len(lines)
    for i in range(0,count):
        process_trade_day(lines, i, days, 6) #6 close

def main(days): 
    stocks = stock_meta.load_all()
    for stock in stocks:
        process_stock(stock['stock_no'],days)
        # print stock

if __name__ == "__main__": 
    main(int(sys.argv[1]))
    # main('600470',1)
