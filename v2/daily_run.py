#!/usr/bin/python
# -*- coding: utf-8 -*-
import config
import download
import loader

if __name__ == "__main__" : 
    # download.download_latest()
    latest_day = '2015-04-13' # config.get_today()
    loader.load_daily_stocks_v2(latest_day)