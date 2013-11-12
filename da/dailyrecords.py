#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log


def update(pk_id,**kv):
    dbw.update('stock_daily_records',where='pk_id=$pk_id',vars=locals(),**kv)

def load_by_date(date):
    return dbr.select('stock_daily_records',what='pk_id,stock_no',where='date=$date',vars=locals())

def load_pkids(date):
    pkids = {}
    rows = load_by_date(date)
    for r in rows:
        pkids[r.stock_no] = r.pk_id
    return pkids

