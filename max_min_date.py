#!/usr/bin/env python
# -*- coding: utf-8 -*-
import da

def gen_new_field_sql():
    print "ALTER TABLE `stock_base_infos`"
    start_field = 'trade_date'
    for d in (7,30,90,188,365,730):
        for t in ('high','low'):
            for s in ('price','date'):
                field_type = 'date' if s=='date' else 'decimal(8,2)'
                print "ADD COLUMN `%s_%s_%s` %s NULL AFTER `%s`," % (t,s,d,field_type,start_field)
                start_field = '%s_%s_%s' % (t,s,d)

    #ADD COLUMN `high_date_7`  date NULL AFTER `trade_date`,
    #ADD COLUMN `high_price_7`  decimal(8,2) NULL AFTER `high_date_7`;

def update_stock_high_low(stock_no):
    d={}
    for day in (7,30,90,188,365,730):
        d.update(da.dailyrecords.load_max_min(stock_no,day))
    da.stockbaseinfos.update_high_low(stock_no,d)

def run():
    stocks = da.stockbaseinfos.load_all_stocks()
    for s in stocks:
        update_stock_high_low(s.stock_no)


if __name__ == '__main__':
    run()
    #gen()

