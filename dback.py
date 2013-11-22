#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from config import dbr,dbw,const_root_local,init_log
import datetime

t = 0

def run():
    date = datetime.datetime.now().strftime('%Y%m%d')
    os.system('mysqldump -uroot -proot -d forecast > %s/db/forecast_%s_%s.sql' % (const_root_local,date,t))

    backtables = ['stock_base_infos','date_sums','date_sum_infos','stock_daily_records','trading_records','trading_strategies_records','trend_daily']
    for table_name in backtables:
        os.system('mysqldump -uroot -proot forecast %s > %s/db/%s_%s_%s.sql'% (table_name,const_root_local,table_name,date,t) )

if __name__ == "__main__":
    run()


# mysqldump -uroot -proot  -d forecast >  forecast.sql
# mysql -uroot -proot forecast -B -e "select * from date_sum_infos" > Documents/date_sum_infos.csv
