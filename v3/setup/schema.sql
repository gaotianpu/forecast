/*
forecast 用到的sqlite库
*/
DROP TABLE if exists stocks;
CREATE TABLE stocks --stocks
( 
    stock_no TEXT PRIMARY KEY NOT NULL,
    trade_start INTEGER NOT NULL
);

DROP TABLE if exists stocks_trade_records;
CREATE TABLE stocks_trade_records --交易记录
(
    id INTEGER PRIMARY KEY NOT NULL, --trade_date+trade_time+stock_no， 201709081000001
    trade_date INTEGER NOT NULL, --交易日期,20170908
    trade_time INTEGER NOT NULL, --交易时间，上午结束0，全天结束1
    stock_no  TEXT NOT NULL, --股票代码 000001 ，399001，600012，002159
    stock_exchange  INTEGER NOT NULL, --股票交易所0深,3创业,6沪, 7指数？9未知
    open REAL NOT NULL, --开盘价
    close REAL NOT NULL, --收盘价
    high REAL NOT NULL, --最高价
    low  REAL NOT NULL, --最低价
    last_close  REAL NOT NULL, --前收盘价
    CHG REAL NOT NULL, --涨跌额 ，收盘价-前收盘价
    PCHG REAL NOT NULL, --涨跌幅 ，(收盘价-前收盘价)/前收盘价
    turn_over REAL NOT NULL, --换手率
    vo_turn_over REAL NOT NULL,--成交量
    va_turn_over REAL NOT NULL,--成交金额
    t_cap REAL NOT NULL, --总市值
    m_cap REAL NOT NULL, --流通市值
    create_time INTEGER NOT NULL, --创建时间 
    update_time INTEGER NOT NULL --,  --变更时间
    -- trade_year INTEGER NOT NULL DEFAULT 0, --交易year,2017，方便统计用？
    -- trade_quarter INTEGER NOT NULL DEFAULT 0, --交易季度,1,2,3,4
    -- trade_month INTEGER NOT NULL DEFAULT 0, --交易月份， 1~12
    -- trade_day_of_month INTEGER NOT NULL DEFAULT 0, --交易日 0~31
    -- trade_day_of_week INTEGER NOT NULL DEFAULT 0 --周几 0~7
);
CREATE INDEX idx_date_stocks_trade_records on stocks_trade_records (trade_date,stock_no);
CREATE INDEX idx_stock_no_stocks_trade_records on stocks_trade_records (stock_no,trade_date);


DROP TABLE if exists stocks_forecast_day1;
CREATE TABLE stocks_forecast_day1 --交易记录
(
    id INTEGER PRIMARY KEY NOT NULL, --trade_date+trade_time+stock_no， 201709081000001
    trade_date INTEGER NOT NULL, --交易日期,20170908 
    stock_no  TEXT NOT NULL, --股票代码 000001 ，399001，600012，002159
    forecast_trade_date INTEGER NOT NULL, 
    forecast_CHG REAL NOT NULL, --涨跌额，收盘价-前收盘价
    forecast_PCHG REAL NOT NULL --涨跌幅，(收盘价-前收盘价)/前收盘价
);

DROP TABLE if exists stocks_forecast_day2;
CREATE TABLE stocks_forecast_day2 --交易记录
(
    id INTEGER PRIMARY KEY NOT NULL, --trade_date+trade_time+stock_no， 201709081000001
    trade_date INTEGER NOT NULL, --交易日期,20170908 
    stock_no  TEXT NOT NULL, --股票代码 000001 ，399001，600012，002159
    forecast_trade_date INTEGER NOT NULL, 
    forecast_CHG REAL NOT NULL, --涨跌额，收盘价-前收盘价
    forecast_PCHG REAL NOT NULL --涨跌幅，(收盘价-前收盘价)/前收盘价
);

DROP TABLE if exists stocks_forecast_day3;
CREATE TABLE stocks_forecast_day3 --交易记录
(
    id INTEGER PRIMARY KEY NOT NULL, --trade_date+trade_time+stock_no， 201709081000001
    trade_date INTEGER NOT NULL, --交易日期,20170908 
    stock_no  TEXT NOT NULL, --股票代码 000001 ，399001，600012，002159
    forecast_trade_date INTEGER NOT NULL, 
    forecast_CHG REAL NOT NULL, --涨跌额，收盘价-前收盘价
    forecast_PCHG REAL NOT NULL --涨跌幅，(收盘价-前收盘价)/前收盘价
);

DROP TABLE if exists stat_trade_days;
CREATE TABLE stat_trade_days --按trade_days统计
(
    trade_date INTEGER PRIMARY KEY NOT NULL, --交易日期,20170908
    all_count INTEGER NOT NULL, --全量数 
    up_count INTEGER NOT NULL, --上升数
    up_percent  REAL NOT NULL, --上升占比
    down_count  INTEGER NOT NULL, --下降数
    down_percent REAL NOT NULL, --下降占比 
    create_time INTEGER NOT NULL --创建时间 
);

DROP TABLE if exists stat_stocks;
CREATE TABLE stat_stocks --按stock_no统计
(
    stock_no  INTEGER PRIMARY KEY NOT NULL, --stock编号
    all_count INTEGER NOT NULL, --交易日数
    up_count INTEGER NOT NULL, --上升天数
    up_percent  REAL NOT NULL, --上升占比
    down_count  INTEGER NOT NULL, --下降天数
    down_percent REAL NOT NULL, --下降占比 
    min_close REAL NOT NULL, --最低收盘价
    max_close REAL NOT NULL, --最高收盘价 #所在交易日？
    min_vo_turn_over REAL NOT NULL, --最低成交量
    max_vo_turn_over REAL NOT NULL, --最高成交量
    create_time INTEGER NOT NULL --创建时间 
);