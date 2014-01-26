#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import datetime
from config import dbr,dbw,const_root_local,init_log

def load_stockno(stockno):
	return list(dbr.select('stock_daily',where='stock_no=$stockno and volume>0', order='trade_date desc',vars=locals()))