#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw,const_root_local,init_log
from datetime import datetime,date,timedelta
import os

import random

loger = init_log("trading")

def load_dates_stock(stock_no,buy_date,hold_days):
    r = dbr.select('stock_daily_records',
        where="stock_no=$stock_no and volume>0 and date>$buy_date", offset=0,limit=hold_days+1,order="date asc", vars=locals())
    return list(r)

def buy_and_sell(strategy_id,strategy_batch_no,stock_no,buy_date,hold_days=1,buy_price='open_price',sell_price='open_price',trade_hands=1):
    stocks = load_dates_stock(stock_no,buy_date,hold_days)
    if len(stocks)< hold_days + 1:
        raise Exception('no-sell-date-stock-info')
    buy_stock = stocks[0]
    sell_stock = stocks[-1]

    earnings = ( sell_stock[sell_price] - buy_stock[buy_price] )*  trade_hands * 100
    earnings_rate = ( sell_stock[sell_price] - buy_stock[buy_price] )/ buy_stock[buy_price] * 100

    dbw.insert('trading_records',
        strategy_id = strategy_id,
        strategy_batch_no = strategy_batch_no,
        buy_or_sell = 0,
        stock_no = buy_stock.stock_no,
        date = buy_stock.date,
        open_or_close = buy_price,
        price = buy_stock[buy_price],
        hands = trade_hands,
        input_output = 0 - buy_stock[buy_price] * trade_hands  * 100 ,
        earnings=earnings,earn_rate=earnings_rate,
        create_date=web.SQLLiteral('now()'))

    dbw.insert('trading_records',
        strategy_id = strategy_id,
        strategy_batch_no = strategy_batch_no,
        stock_no = sell_stock.stock_no,
        buy_or_sell = 1,
        date = sell_stock.date,
        open_or_close = sell_price,
        price = sell_stock[sell_price],
        hands = trade_hands,
        input_output =  sell_stock[sell_price] * trade_hands  * 100 ,
        earnings = earnings, earn_rate=earnings_rate,
        create_date=web.SQLLiteral('now()'))

def run_strategy_sum(strategy_id):
    sql='''update trading_strategies s,
(select strategy_id,max(earn_rate) as max_earn_rate,
    min(earn_rate) as min_earn_rate,
    sum(earnings)/sum(input_output)*100 as avg_earn_rate,
    count(*) as trade_count from `trading_records` where strategy_id=%s and buy_or_sell=1) as ss
set s.max_earn_rate=ss.max_earn_rate,
s.min_earn_rate = ss.min_earn_rate,
s.avg_earn_rate = ss.avg_earn_rate,
s.trade_count = ss.trade_count,
s.last_update = now()
where s.pk_id=ss.strategy_id;
    ''' % (strategy_id)
    dbw.query(sql)

##################################

def backup_tradingrecords(strategy_id):
    table_name = 'trading_records'
    os.system('mysqldump -uroot -proot forecast %s > %s/db/%s_%s.sql'% (table_name,const_root_local,table_name,strategy_id) )
    dbw.delete('trading_records',where="pk_id>0")

def run_strategy_tradding(strategy_id,dates,stock_nos):
    for i in range(0,1000):
        stock_no = random.choice(stock_nos)
        date = random.choice(dates)
        try:
            buy_and_sell(strategy_id,i,stock_no,date)
        except Exception,e:
            print e
            loger.error("stock_no=%s&date=%s&error=%s" %(stock_no,date,e))
    run_strategy_sum(strategy_id)
    backup_tradingrecords(strategy_id)


def run_strategy_1(year):
    strategy_id = dbw.insert('trading_strategies',title="random_%s" % (year),description="YEAR(date)=%s,market_code_yahoo in ('ss','sz')"% (year))
    dates = [r.date for r in  dbr.select('date_sum_infos',what="date",where="YEAR(date)=%s" % (year) )]
    stock_nos = [r.stock_no for r in  dbr.select('stock_base_infos',what="stock_no",where="market_code_yahoo in ('ss','sz')")]
    run_strategy_tradding(strategy_id,dates,stock_nos)

def run_year():
    for year in range(1990,2013):
        run_strategy_1(year)

## 2013_price_up_percent_0_20
def run_price_up_percent(strCondition,title,description):
    strategy_id = dbw.insert('trading_strategies',title=title,description=description,create_date=web.SQLLiteral('now()'))
    dates = [r.date for r in  dbr.select('date_sum_infos',what="date",where=strCondition)]
    stock_nos = [r.stock_no for r in  dbr.select('stock_base_infos',what="stock_no",where="market_code_yahoo in ('ss','sz')")]
    run_strategy_tradding(strategy_id,dates,stock_nos)

def run_strategy_2():
    cdd = "YEAR(date)=2013 and price_up_percent<20"
    run_price_up_percent(cdd,"2013_price_up_percent_0_20","%s,market_code_yahoo in ('ss','sz')" % (cdd))
    return
    cdd = "YEAR(date)=2013 and price_up_percent>20 and  price_up_percent<=40"
    run_price_up_percent(cdd,"2013_price_up_percent_20_40","%s,market_code_yahoo in ('ss','sz')" % (cdd))

    cdd = "YEAR(date)=2013 and price_up_percent>40 and  price_up_percent<=60"
    run_price_up_percent(cdd,"2013_price_up_percent_40_60","%s,market_code_yahoo in ('ss','sz')" % (cdd))

    cdd = "YEAR(date)=2013 and price_up_percent>60 and  price_up_percent<=80"
    run_price_up_percent(cdd,"2013_price_up_percent_60_80","%s,market_code_yahoo in ('ss','sz')" % (cdd))

    cdd = "YEAR(date)=2013 and price_up_percent>80"
    run_price_up_percent(cdd,"2013_price_up_percent_80_100","%s,market_code_yahoo in ('ss','sz')" % (cdd))


if __name__ == "__main__":
    run_year()
    #run_strategy_1()
    #run_strategy_2()
    #run_strategy_sum(1)
    #buy_and_sell(1,1,600000,'2013-09-23',1)
    #print random.randrange(1000)
    #run(filter_stocks_func,strategy,date)


