#!/usr/bin/env python
# -*- coding: utf-8 -*-
import da
import comm

def run():
    dates = da.stockdaily_cud.load_trade_dates()
    today = dates[0].trade_date    
    date_3 = dates[2].trade_date      

    date_3_rows = da.stockdaily_cud.load_by_beginDate(date_3)

    stocks = da.stockbaseinfos.load_all_stocks() #[web.storage(stock_no='000001',pk_id=332)] #test
    for s in stocks:
        rows = [r for r in date_3_rows if r.stock_no==s.stock_no]
        if not rows:
            continue
        print s.stock_no,comm.get_trend(rows)
        da.stockdaily_cud.update_trend3(today,s.stock_no,comm.get_trend(rows)) 


if __name__ == "__main__":
    run()
