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


def get_stock_exchange(stock_no):
    """转换exchange,公共方法？"""
    if stock_no.startswith('0'):
        return 0
    if stock_no.startswith('3'):
        return 3
    if stock_no.startswith('6'):
        return 6
    return 9  # 未知