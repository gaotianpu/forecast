#!/usr/bin/env python
# -*- coding: utf-8 -*-
import da
from config import dbr,dbw,const_root_local,init_log
import datetime

def load_daily_records():
    #SELECT * FROM `stock_daily_records` order by date asc limit 0,1000 ;
    results = dbr.select('stock_daily_records',order='date asc',limit=1000,offset=0)
    return list(results)

def replace_z_records(record):
    #date,stock_no,open_price,high_price,low_price,close_price,volume,amount,adj_close,
    #raise_drop,raise_drop_rate,is_traday,volume_updown,volume_updown_rate,create_date,last_update
    strfields = 'date,stock_no,open_price,high_price,low_price,close_price,volume,amount,adj_close,raise_drop,raise_drop_rate,is_traday,volume_updown,volume_updown_rate,create_date,last_update'
    fields = strfields.split(',')

    sql="replace into z_%s set %s" % (record.stock_no, ','.join(["%s='%s'" % (k,v)  for k,v in record.items() if k in fields and v is not None]))
    dbw.query(sql)


def delete_daily_record(pk_id):
    dbw.delete('stock_daily_records',where='pk_id=$pk_id',vars=locals())

loger = init_log("remove_data")

def run(end_date):
    rows = load_daily_records()
    for r in rows:
        if r.date >  end_date :
            print 'date big than 2013-1-1'
            return False
            break
        try:
            replace_z_records(r)
            delete_daily_record(r.pk_id)
        except Exception,ex:
            print '%s %s' %(r.pk_id,str(ex))
            loger.error('%s %s' %(r.pk_id,str(ex)))

    return len(rows)

def run_more(end_date):
    while True:
        result = run()
        if not result:
            break

if __name__ == '__main__':
    run_more(datetime.date(2013,1,1) )

