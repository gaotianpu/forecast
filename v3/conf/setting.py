#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置信息
"""

#从网易数据下载到的原始的字段
RAW_FIELDS_SORT="trade_date,stock_no,stock_name,close,high,low,open,last_close,CHG,PCHG,turn_over,vo_turn_over,va_turn_over,t_cap,m_cap"

#转换后的字段
FIELDS_SORT = ("id,trade_date,trade_time,stock_no,stock_exchange,open,close,high,low,last_close,"
               "CHG,PCHG,turn_over,vo_turn_over,va_turn_over,t_cap,m_cap,create_time,update_time"
               )

# 所有股票
STOCKS_ALL = 'data/all_stocks.csv'
# http://www.sse.com.cn/assortment/stock/list/share/
# http://www.szse.cn/main/marketdata/jypz/colist/
# 从沪深两市官网下载excel整理

# 历史数据源
HISTORY_DATA_URL = ''
# http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html?year=2017&season=3
# http://quotes.money.163.com/service/chddata.html?code=0000001&start=19901219&end=20170929&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER
# http://quotes.money.163.com/service/chddata.html?code=1399001&start=19910403&end=20170929&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER
# http://quotes.money.163.com/service/chddata.html?code=1300184&start=20110222&end=20170929&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
# http://quotes.money.163.com/service/chddata.html?code=0600012&start=20030107&end=20171001&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
# http://quotes.money.163.com/service/chddata.html?code=1002159&start=20070817&end=20171001&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP

'''
TCLOSE; 收盘价
HIGH; 最高价
LOW; 最低价
TOPEN; 开盘价
LCLOSE; 前收盘价
CHG; 涨跌额
PCHG; 涨跌幅
TURNOVER; 换手率
VOTURNOVER; 成交量
VATURNOVER; 成交金额
TCAP; 总市值
MCAP 流通市值
'''


# 最新数据源
NEW_DATA_URL = 'http://hq.sinajs.cn/list='
# http://hq.sinajs.cn/list=sh600000,sh600004,sh600005,sh600006,sh600007,sh600008,sh600009,sh600010,sh600011,sh600012,sh600015,sh600016,sh600017,sh600018,sh600019,sh600020,sh600021,sh600022,sh600026,sh600027,sh600028,sh600029,sh600030,sh600031,sh600033,sh600035,sh600036,sh600037,sh600038,sh600039,sh600048,sh600050,sh600052,sh600053,sh600054,sh600055,sh600056,sh600057,sh600059,sh600060,sh600061,sh600062,sh600063,sh600064,sh600066,sh600067,sh600068,sh600069,sh600070,sh600071,sh600072,sh600073,sh600075,sh600076,sh600077,sh600078,sh600079,sh600080,sh600081,sh600082,sh600083,sh600084,sh600085,sh600086,sh600088,sh600089,sh600090,sh600091,sh600093,sh600094,sh600095,sh600096,sh600097,sh600098,sh600099,sh600100,sh600101,sh600103,sh600104,sh600105,sh600106,sh600107,sh600108,sh600109,sh600110,sh600111,sh600112,sh600113
# http://api.money.126.net/data/feed/0000001,0600012,1300184,1002902,0601857,0601600,0601398,0600028,0600019,0601318,0600030,0601939,0601088,0600900,1002024,0603136,0600593,0603869,1000888,1002159,money.api?callback=_ntes_quote_callback7451091
