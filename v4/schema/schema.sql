/* sqlite3 https://www.runoob.com/sqlite/sqlite-tutorial.html
sqlite3 database.db
.tables
.separator ","  #指定分隔符为","
.import history_import/600012.csv stocks_daily
*/

/*1. stocks: pkid,stock_no,stock_name,start_date*/
drop table stocks;
CREATE TABLE stocks(
   pkid INT PRIMARY KEY NOT NULL, 
   stock_no VARCHAR(10) NOT NULL,
   stock_name VARCHAR(20) NOT NULL,
   start_date DATE NOT NULL
);
CREATE UNIQUE INDEX index_stock_no on stocks (stock_no);


/*2. stocks_daily: pkid,stock_no,date,收盘价 close,最高价 high,最低价 low,开盘价 open,前收盘 last_close,
涨跌额 CHG;涨跌幅 PCHG;换手率 TURNOVER;成交量 VOTURNOVER;成交金额 VATURNOVER;总市值 TCAP;流通市值 MCAP
pkid INTEGER PRIMARY KEY AUTOINCREMENT,*/
drop table stocks_daily;
CREATE TABLE stocks_daily(  
   stock_no VARCHAR(10) NOT NULL,
   date DATE NOT NULL, 
   close NUMERIC NOT NULL, --收盘价 close 
   high NUMERIC NOT NULL, --最高价 high
   low NUMERIC NOT NULL,
   open NUMERIC NOT NULL,
   last_close NUMERIC NOT NULL,
   CHG NUMERIC NOT NULL,
   PCHG NUMERIC NOT NULL,
   TURNOVER NUMERIC NOT NULL,
   VOTURNOVER NUMERIC NOT NULL,
   VATURNOVER NUMERIC NOT NULL,
   TCAP NUMERIC NOT NULL,
   MCAP NUMERIC NOT NULL
);
CREATE UNIQUE INDEX index_stock_daily on stocks_daily (stock_no,date);
CREATE INDEX index_stock_daily_stock_date on stocks_daily (date);