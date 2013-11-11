#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log

def load_all_stocks():
    return list(dbr.select('stock_base_infos',
        what='stock_no,market_code,market_code_yahoo,pinyin2',
        where="days<>0",
        #where="market_code_yahoo in ('ss','sz')",
        #offset=0,limit=1,
        order="market_code,stock_no"))


def import_daily_records(table,rows):
    dbw.supports_multiple_insert = True
    dbw.multiple_insert(table,rows)

if __name__ == '__main__':
     load_all_stocks()

