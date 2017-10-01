/*
forecast 用到的sqlite库
*/

DROP TABLE if exists stocks_trade_records;
CREATE TABLE stocks_trade_records --交易记录
(
    trade_date INTEGER NOT NULL, --交易日期,20170908
    trade_time INTEGER NOT NULL, --交易时间，上午结束0，全天结束1
    stock_no  INTEGER NOT NULL, --股票代码 000001 ，399001，600012，002159
    stock_exchange  INTEGER NOT NULL, --股票交易所0深,3创业,6沪, 7指数？9未知
    open REAL NOT NULL, --开盘价
    close REAL NOT NULL, --收盘价
    high REAL NOT NULL, --最高价
    low  REAL NOT NULL, --最低价
    last_close  REAL NOT NULL, --前收盘价
    CHG REAL NOT NULL, --涨跌额，收盘价-前收盘价
    PCHG REAL NOT NULL, --涨跌幅，(收盘价-前收盘价)/前收盘价
    turn_over REAL NOT NULL, --换手率
    vo_turn_over REAL NOT NULL,--成交量
    va_turn_over REAL NOT NULL,--成交金额
    t_cap REAL NOT NULL, --总市值
    m_cap REAL NOT NULL, --流通市值
    create_time INTEGER NOT NULL, --创建时间 
    update_time INTEGER NOT NULL  --变更时间
);
CREATE INDEX idx_date_stocks_trade_records on stocks_trade_records (trade_date,stock_no);
CREATE INDEX idx_stock_no_stocks_trade_records on stocks_trade_records (stock_no,trade_date);