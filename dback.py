#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from config import dbr,dbw,const_root_local,init_log
import datetime

t = 0

def run():
    date = datetime.datetime.now().strftime('%Y%m%d')
    os.system('mysqldump -uroot -proot -d forecast > %s/db/forecast_%s_%s.sql' % (const_root_local,date,t))
    os.system('mysqldump -uroot -proot forecast stock_base_infos > %s/db/stock_base_infos_%s_%s.sql'% (const_root_local,date,t) )
    os.system('mysqldump -uroot -proot forecast stock_daily_records > %s/db/stock_daily_records_%s_%s.sql'% (const_root_local,date,t))

if __name__ == "__main__":
    run()
