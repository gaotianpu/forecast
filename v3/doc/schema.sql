
--20180104,1000001,13.25,13.35,0.00754716981132
--trade_date,stock_no,close,high,rate
CREATE TABLE `future` (
  `trade_date` int(11) DEFAULT NULL,
  `stock_no` int(11) NOT NULL DEFAULT '0',
  `close` decimal(8,2) NOT NULL DEFAULT '0.00',
  `high` decimal(8,2) NOT NULL DEFAULT '0.00',
  `rate` float NOT NULL DEFAULT '0',
  UNIQUE KEY `date_stock` (`trade_date`,`stock_no`),
  KEY `stock_no` (`stock_no`,`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;