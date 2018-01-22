
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

--last_data[0,0],future_rate,wave_range,mean_range,start_range,end_range,vol_zscore
CREATE TABLE `train_data` (
  `trade_date` int(11) DEFAULT NULL,
  `stock_no` int(11) NOT NULL DEFAULT '0',
  `future_rate` float NOT NULL DEFAULT '0.00',
  `wave_range` float NOT NULL DEFAULT '0.00',
  `mean_range` float NOT NULL DEFAULT '0',
  `start_range` float NOT NULL DEFAULT '0',
  `end_range` float NOT NULL DEFAULT '0',
  `vol_zscore` float NOT NULL DEFAULT '0',
  UNIQUE KEY `date_stock` (`trade_date`,`stock_no`),
  KEY `stock_no` (`stock_no`,`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;