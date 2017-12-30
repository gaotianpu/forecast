#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置文件
"""
import os
import logging

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)

DATA_ROOT = home_dir + '/data'
LOG_ROOT = home_dir + '/log'

HISTORY_DATA_PATH = DATA_ROOT + '/history' 
HISTORY_CONVERTED_PATH = DATA_ROOT + '/converted'
FUTURE_PATH = DATA_ROOT + '/future'


log_level=logging.DEBUG #日志级别


NEW_DATA_PATH = DATA_ROOT + '/new'


ALL_STOCKS_FILE = DATA_ROOT + '/all_stocks.csv'
SQLITE3_DB_FILE= DATA_ROOT + '/FORECAST.db'
