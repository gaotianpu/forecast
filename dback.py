#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from config import dbr,dbw,const_root_local,init_log
import datetime

t = 0

def run():
    date = datetime.datetime.now().strftime('%Y%m%d')
    os.system('mysqldump -uroot -proot -d forecast > %s/db/forecast_%s_%s.sql' % (const_root_local,date,t))

    for table_name in ['stock_base_infos','stock_daily_records','trading_records','trading_strategies_records']:
        os.system('mysqldump -uroot -proot forecast %s > %s/db/%s_%s_%s.sql'% (table_name,const_root_local,table_name,date,t) )

if __name__ == "__main__":
    run()


# mysqldump -uroot -proot  -d forecast >  forecast.sql
