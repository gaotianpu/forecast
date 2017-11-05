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
import csv


def get_stock_exchange(stock_no):
    """转换exchange,公共方法？"""
    if stock_no.startswith('0'):
        return 0
    if stock_no.startswith('3'):
        return 3
    if stock_no.startswith('6'):
        return 6
    return 9  # 未知


def load_all(file_path):
    """读取本地数据 公共方法？"""
    with open(file_path) as f:
        for i, line in enumerate(f):
            if i != 0:
                yield line.strip().split(',')


def load_csv(csvfile, fieldnames=None):
    with open(csvfile) as f:
        reader = csv.DictReader(f, fieldnames)
        for row in reader:
            yield row
