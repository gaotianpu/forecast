#!/usr/bin/env python
# -*- coding: utf-8 -*-
import da
from config import dbr,dbw,const_root_local,init_log

#create tables
def create_table(stock_no):
    dbw.query("DROP TABLE IF EXISTS `z_%s`;" % (stock_no))
    sql = """CREATE TABLE `z_%s` (
  `date` date NOT NULL DEFAULT '0000-00-00',
  `stock_no` varchar(10) DEFAULT NULL,
  `open_price` decimal(8,2) DEFAULT NULL,
  `high_price` decimal(8,2) DEFAULT NULL,
  `low_price` decimal(8,2) DEFAULT NULL,
  `close_price` decimal(8,2) DEFAULT NULL,
  `volume` bigint(11) DEFAULT NULL,
  `amount` bigint(11) DEFAULT NULL,
  `adj_close` decimal(8,2) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  `raise_drop` decimal(8,2) DEFAULT NULL,
  `raise_drop_rate` decimal(7,3) DEFAULT NULL,
  `is_traday` int(11) DEFAULT NULL,
  `volume_updown` bigint(11) DEFAULT NULL,
  `volume_updown_rate` decimal(30,2) DEFAULT NULL,
  PRIMARY KEY (`date`),
  KEY `volume_idx` (`volume`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (stock_no)
    dbw.query(sql)

def create_tables():
    rows = da.stockbaseinfos.load_all_stocks()
    for r in rows:
        create_table(r.stock_no)

#import history records
def import_trade_record(stock_no,rows):
    sql = "replace into z_% (date,stock_no,open_price,high_price,low_price,close_price,volume,amount,adj_close)values()" % (stock_no)
    dbw.query(sql)


if __name__ == '__main__':
    create_tables()
