#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

#定义一些配置量
#
stocks_list_file = "/Users/gaotianpu/github/forecast/v2/all_stocks_list.txt"  #存放所有stock列表
local_root_dir = "/Users/gaotianpu/Documents/stocks/"  #数据下载存储位置
history_data_dir = local_root_dir + "history/"  #单只stock历史数据存放位置
daily_data_dir = local_root_dir + "daily/" #每天所有stocks数据存放目录

history_price_change_rate_dir = local_root_dir + "history_price_change_rate/" #每天所有stocks数据存放目录
latest_data_dir = local_root_dir + "latest/" #

def get_today():
    today = datetime.datetime.now()
    trade_date = today.strftime('%Y-%m-%d')
    return trade_date