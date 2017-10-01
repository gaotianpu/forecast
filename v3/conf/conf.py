#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置文件
"""
import os
home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)

DATA_ROOT = home_dir + '/data'
HISTORY_DATA_PATH = DATA_ROOT + '/history'
ALL_STOCKS_FILE = DATA_ROOT + '/all_stocks.csv'
