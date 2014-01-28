#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
import comm

urls = (
    '/candle','Candle',
    '/','Index')

render = web.template.render('templates')

class Index:
    def GET(self):
    	r = web.storage(stocks=[],query='',count=0) 
     	return render.index(r)
    def POST(self):
    	i = web.input(sql="")
    	rows = list(dbr.query(i.sql))

    	l = []
    	for r in rows:
    		code = comm.get_market_codes(r.stock_no)
        	if not code['pinyin'] : continue
        	l.append(web.storage(stock_no=r.stock_no,pinyin2=code['pinyin']) )    		 

    	r = web.storage(stocks=l,query=i.sql,count = len(l)) 
     	return render.index(r)

class Candle:
    def GET(self):
        rows = list(dbr.select('stock_daily',what='candle_sort,range_1,range_2,range_3',
            where="volume>0 and stock_no='002639'",
            offset=0,limit=2000,order="trade_date asc",vars=locals()))
        for r in rows:
            r.updown = "up" if r.range_2>0 else "down"
            print r.range_2
            
        r = web.storage(rows=rows,query='',count=len(rows)) 
        return render.candle(r)


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()