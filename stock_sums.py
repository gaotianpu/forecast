#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log

funs = ['max','min']
days = [2,3,5,10,15,30,60]
fields = {'price':'decimal(8,2)','volumn':'bigint(16)'}

sql_t='''CREATE TABLE `stock_sums_info` (
  `pk_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `stock_no` varchar(11) DEFAULT NULL,
  %s ,
  `create_date` datetime DEFAULT NULL,  
  `last_update` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `stock_no_idx` (`stock_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

def create_table_sql():
    l = []
    for fun in funs:
        for field,ftype in fields.items():
            for day in days:
                field_final = '%s_%s_%s' % (fun,field,day)
                segment = "`%s` %s DEFAULT NULL" % (field_final,ftype)
                print segment
                l.append(segment)
    dbw.query(''' DROP TABLE IF EXISTS `stock_sums_info` ''')
    dbw.query(sql_t % (','.join(l)))  

def load_sum(stock_no,days):
    dbr.select('stock_sums_info',
        what="max(open_price) as max_price,min(open_price) as min_price,max(volume) as max_volume,min(volume) as min_volume"),
        where="")

if __name__ == "__main__":
    create_table_sql()