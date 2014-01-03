#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
import comm

urls = ('/','Index')
render = web.template.render('templates')

class Index:
    def GET(self):
    	r = web.storage(stocks=[],query='',count=0) 
     	return render.index(r)
    def POST(self):
    	i = web.input(sql="")
    	rows = list(dbr.select('stock_daily',
    		where="trade_date='2014-1-3' and volume<>0 and (" + i.sql + ")",
    		vars=locals()))

    	l = []
    	for r in rows:
    		code = comm.get_market_codes(r.stock_no)
        	if not code['pinyin'] : continue
        	l.append(web.storage(stock_no=r.stock_no,pinyin2=code['pinyin']) )    		 

    	r = web.storage(stocks=l,query=i.sql,count = len(l)) 
     	return render.index(r)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()