

select max(high),min(low),avg(close),
max(vo_turn_over),min(vo_turn_over),avg(vo_turn_over)
from (
select * from stocks_trade_records where stock_no='600004' order by trade_date desc limit 15) 
as t;

select high,low,close from stocks_trade_records where stock_no='600004' order by trade_date desc limit 15