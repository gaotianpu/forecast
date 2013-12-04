#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import datetime
from config import const_root_local,init_log,dbr,dbw
import util

fields = ['high_date_7','high_date_30','high_date_90','high_date_188','high_date_365','low_date_7','low_date_30','low_date_90','low_date_188','low_date_365']

comm_codition =" volumn<>0 and market_code is not null "

def __get_plate_cout(field_name):
    sql="""SELECT market_code,count(*) as %s_count  FROM `stock_base_infos` 
    where %s=trade_date and %s
    group by market_code 
    order by count(*) desc;""" % (field_name,field_name,comm_codition)
    return list(dbr.query(sql))

def get_all_plate_count():
    l=[]     
    for f in fields:
        l = l + __get_plate_cout(f)
    return l 

sql_seg="round(avg(open),2) as avg_open,round(avg(close),2) as avg_close,round(avg(high),2) as avg_high,round(avg(low),2) as avg_low,round(avg(volumn),0) as avg_volume,round(avg(amount),0) as avg_amount"
def get_market_avg():
    sql="select market_code,count(*) as count,%s from `stock_base_infos` where %s group by market_code;" % (sql_seg,comm_codition)
    return list(dbr.query(sql))

def get_all_avg():
    sql="select 'ALL' as market_code,count(*) as count,%s from `stock_base_infos` where %s ;" % (sql_seg,comm_codition)
    return list(dbr.query(sql))

def close_high_than_open():
    sql="select market_code,count(*) as cho_count from `stock_base_infos` where %s and close>open group by market_code;"  % (comm_codition)
    return list(dbr.query(sql))

####
plates = ['cyb','ha','sa','zxb','sb']
def convert(rows):
    l = []
    for r in rows:         
        r.market_code
        for k,v in r.items():
            if k <> "market_code":                
                l.append((r.market_code,k,v))
    return l

def run():
    l = convert(get_all_plate_count())     
    l = l + convert(get_market_avg())
    l = l + convert(close_high_than_open())

    data = web.storage(day=datetime.datetime.now().strftime('%Y-%m-%d'),rows=l,
        row_names=['count','cho_count','avg_open','avg_close','avg_high','avg_low','avg_volume','avg_amount','high_date_365_count','high_date_188_count','high_date_90_count','high_date_30_count','high_date_7_count','low_date_365_count','low_date_188_count','low_date_90_count','low_date_30_count','low_date_7_count'],
        column_names = ['cyb','ha','sa','zxb'])
    render_sum = web.template.frender('templates/sum.html')
    content = str(render_sum(data))     

    subject='sum_%s' % ( datetime.datetime.now().strftime('%Y-%m-%d') )
    util.emailsmtp.sendmail(subject,content,['462042991@qq.com']) 

if __name__ == "__main__":   
    run()
    