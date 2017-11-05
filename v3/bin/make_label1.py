#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
根据未来n天的涨幅，决定分类标签，up-1，down-0
trade_date + stock_no, 未来一天，未来2天，未来3天的涨幅，生成label?

网易数据源
"""
import os
import sys
import pandas as pd 
import numpy as np 

import common
import stock_meta

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)

sys.path.append(home_dir + "/conf")
import conf
import setting

fields = setting.FIELDS_SORT.split(',')

def process_stock(stock_no):
    csv_file = "%s/convert_%s.csv" % (conf.HISTORY_CONVERTED_PATH,stock_no)

    myData = np.genfromtxt(csv_file,delimiter=",")  
    print myData[0]

    return 

    df = pd.read_csv(csv_file,header=None,names=fields)
    # print df['close']
    lc=pd.DataFrame(df)
    print lc.sort( ['close'] ).head()
    # print df.head()

    # lines = common.load_all()
    # lines = list(lines)
    # count = len(lines)
    # for i in range(0,count):
    #     process_trade_day(lines, i, days, 6) #6 close

# def main(): 
#     stocks = stock_meta.load_all()
#     for stock in stocks:
#         process_stock(stock['stock_no'],days)
        # print stock

if __name__ == "__main__": 
    process_stock("000001")
    # main(int(sys.argv[1]))