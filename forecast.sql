-- MySQL dump 10.13  Distrib 5.7.2-m12, for Win64 (x86_64)
--
-- Host: localhost    Database: forecast
-- ------------------------------------------------------
-- Server version	5.7.2-m12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `date_avgs`
--

DROP TABLE IF EXISTS `date_avgs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `date_avgs` (
  `date` date DEFAULT NULL,
  `plate` varchar(255) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `open_price` decimal(8,2) DEFAULT NULL,
  `high_price` decimal(8,2) DEFAULT NULL,
  `low_price` decimal(8,2) DEFAULT NULL,
  `close_price` decimal(8,2) DEFAULT NULL,
  `volume` bigint(20) DEFAULT NULL,
  KEY `ix_date` (`date`),
  KEY `ix_plate` (`plate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `date_sum_infos`
--

DROP TABLE IF EXISTS `date_sum_infos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `date_sum_infos` (
  `pk_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `plate` varchar(11) DEFAULT NULL,
  `total_count` int(11) DEFAULT NULL,
  `price_up_count` int(11) DEFAULT NULL,
  `price_up_percent` float DEFAULT NULL,
  `volumn_up_count` int(11) DEFAULT NULL,
  `volumn_up_percent` float DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT NULL,
  `avg_open_price` decimal(8,2) DEFAULT NULL,
  `avg_high_price` decimal(8,2) DEFAULT NULL,
  `avg_low_price` decimal(8,2) DEFAULT NULL,
  `avg_close_price` decimal(8,2) DEFAULT NULL,
  `avg_volume` int(11) DEFAULT NULL,
  `avg_raise_drop` decimal(8,2) DEFAULT NULL,
  `avg_raise_drop_rate` decimal(8,2) DEFAULT NULL,
  `avg_volume_updown` decimal(8,2) DEFAULT NULL,
  `avg_volume_updown_rate` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `date_idx` (`date`),
  KEY `plate_idx` (`plate`)
) ENGINE=MyISAM AUTO_INCREMENT=5587 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `date_sums`
--

DROP TABLE IF EXISTS `date_sums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `date_sums` (
  `trade_date` date NOT NULL DEFAULT '0000-00-00',
  `stock_plate` varchar(11) NOT NULL DEFAULT '',
  `stock_count` int(11) DEFAULT NULL,
  `avg_open` decimal(8,2) DEFAULT NULL,
  `avg_close` decimal(8,2) DEFAULT NULL,
  `avg_high` decimal(8,2) DEFAULT NULL,
  `avg_low` decimal(8,2) DEFAULT NULL,
  `avg_volume` int(11) DEFAULT NULL,
  `avg_amount` int(11) DEFAULT NULL,
  `price_up_count` int(11) DEFAULT NULL,
  `price_up_percent` float DEFAULT NULL,
  `volumn_up_count` int(11) DEFAULT NULL,
  `volumn_up_percent` float DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`trade_date`,`stock_plate`),
  KEY `date_idx` (`trade_date`),
  KEY `plate_idx` (`stock_plate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_base_infos`
--

DROP TABLE IF EXISTS `stock_base_infos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_base_infos` (
  `pk_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `market_code_yahoo` varchar(5) DEFAULT NULL,
  `market_code` varchar(5) DEFAULT NULL,
  `pinyin2` varchar(5) DEFAULT NULL,
  `stock_no` varchar(10) DEFAULT NULL,
  `stock_name` varchar(20) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  `open` decimal(8,2) DEFAULT NULL,
  `close` decimal(8,2) DEFAULT NULL,
  `high` decimal(8,2) DEFAULT NULL,
  `low` decimal(8,2) DEFAULT NULL,
  `volumn` int(8) DEFAULT NULL,
  `amount` decimal(16,2) DEFAULT NULL,
  `lclose` decimal(8,2) DEFAULT NULL,
  `prate` decimal(8,2) DEFAULT NULL,
  `candle` int(11) DEFAULT '0',
  `high_date_7` date DEFAULT NULL,
  `low_price_7` decimal(8,2) DEFAULT NULL,
  `low_date_7` date DEFAULT NULL,
  `high_price_30` decimal(8,2) DEFAULT NULL,
  `high_date_30` date DEFAULT NULL,
  `low_price_30` decimal(8,2) DEFAULT NULL,
  `low_date_30` date DEFAULT NULL,
  `high_price_90` decimal(8,2) DEFAULT NULL,
  `high_date_90` date DEFAULT NULL,
  `low_price_90` decimal(8,2) DEFAULT NULL,
  `low_date_90` date DEFAULT NULL,
  `high_price_188` decimal(8,2) DEFAULT NULL,
  `high_date_188` date DEFAULT NULL,
  `low_price_188` decimal(8,2) DEFAULT NULL,
  `low_date_188` date DEFAULT NULL,
  `high_price_365` decimal(8,2) DEFAULT NULL,
  `high_date_365` date DEFAULT NULL,
  `low_price_365` decimal(8,2) DEFAULT NULL,
  `low_date_365` date DEFAULT NULL,
  `high_price_730` decimal(8,2) DEFAULT NULL,
  `high_date_730` date DEFAULT NULL,
  `low_price_730` decimal(8,2) DEFAULT NULL,
  `low_date_730` date DEFAULT NULL,
  `high_low_update_date` datetime DEFAULT NULL,
  `days_count_5` int(11) DEFAULT NULL,
  `trend_5` int(11) DEFAULT NULL,
  `trend_3` int(11) DEFAULT NULL,
  `prate_3` decimal(8,2) DEFAULT NULL,
  `prate_5` decimal(8,2) DEFAULT NULL,
  `ratetrend_date` datetime DEFAULT NULL,
  `trade_date` date DEFAULT NULL,
  `days` int(11) DEFAULT NULL,
  `high_price_7` decimal(8,2) DEFAULT NULL,
  `gua64` bigint(20) DEFAULT NULL,
  `tengan100` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`pk_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2298 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_daily`
--

DROP TABLE IF EXISTS `stock_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_daily` (
  `pk_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `trade_date` date NOT NULL,
  `stock_no` varchar(10) NOT NULL,
  `open` decimal(8,2) DEFAULT NULL,
  `close` decimal(8,2) DEFAULT NULL,
  `high` decimal(8,2) DEFAULT NULL,
  `low` decimal(8,2) DEFAULT NULL,
  `volume` int(8) DEFAULT NULL,
  `amount` decimal(16,2) DEFAULT NULL,
  `last_close` decimal(16,2) DEFAULT NULL,
  `high_low` decimal(8,2) DEFAULT NULL,
  `close_open` decimal(8,2) DEFAULT NULL,
  `open_last_close` decimal(8,2) DEFAULT NULL,
  `jump_rate` float DEFAULT NULL,
  `price_rate` float DEFAULT NULL,
  `high_rate` float DEFAULT NULL,
  `low_rate` float DEFAULT NULL,
  `hig_low_rate` float DEFAULT NULL,
  `range_1` int(8) DEFAULT NULL,
  `range_2` int(8) DEFAULT NULL,
  `range_3` int(8) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  `last_high_low` decimal(8,2) DEFAULT NULL,
  `trend_3` int(11) DEFAULT NULL,
  `trend_5` int(11) DEFAULT NULL,
  `volume_avg_10` int(11) DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `ix_trade_date` (`trade_date`),
  KEY `ix_stock_no` (`stock_no`)
) ENGINE=MyISAM AUTO_INCREMENT=10073 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_daily_records`
--

DROP TABLE IF EXISTS `stock_daily_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_daily_records` (
  `pk_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `stock_market_no` varchar(5) DEFAULT NULL,
  `stock_no` varchar(10) DEFAULT NULL,
  `open_price` decimal(8,2) DEFAULT NULL,
  `high_price` decimal(8,2) DEFAULT NULL,
  `low_price` decimal(8,2) DEFAULT NULL,
  `close_price` decimal(8,2) DEFAULT NULL,
  `volume` bigint(11) DEFAULT NULL,
  `amount` bigint(11) DEFAULT NULL,
  `adj_close` decimal(8,2) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  `raise_drop` decimal(8,2) DEFAULT NULL,
  `raise_drop_rate` decimal(7,3) DEFAULT NULL,
  `is_traday` int(11) DEFAULT NULL,
  `volume_updown` bigint(11) DEFAULT NULL,
  `volume_updown_rate` decimal(30,2) DEFAULT NULL,
  `gua64` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `date_idx` (`date`),
  KEY `volume_idx` (`volume`),
  KEY `stock_no_idx` (`stock_no`)
) ENGINE=MyISAM AUTO_INCREMENT=5262216 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_daily_records_tmp`
--

DROP TABLE IF EXISTS `stock_daily_records_tmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_daily_records_tmp` (
  `pk_id` int(11) unsigned NOT NULL,
  `raise_drop` decimal(8,2) DEFAULT NULL,
  `raise_drop_rate` decimal(7,3) DEFAULT NULL,
  `volume_updown` bigint(11) DEFAULT NULL,
  `volume_updown_rate` decimal(11,3) DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trading_records`
--

DROP TABLE IF EXISTS `trading_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trading_records` (
  `pk_id` bigint(16) unsigned NOT NULL AUTO_INCREMENT,
  `strategy_id` int(11) DEFAULT NULL,
  `strategy_batch_no` int(11) DEFAULT NULL,
  `buy_or_sell` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `stock_no` varchar(11) DEFAULT NULL,
  `open_or_close` varchar(11) DEFAULT NULL,
  `price` decimal(8,2) DEFAULT NULL,
  `hands` int(11) DEFAULT NULL,
  `input_output` int(11) DEFAULT NULL,
  `earnings` int(11) DEFAULT NULL,
  `earn_rate` float DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `strategy_id_idx` (`strategy_id`),
  KEY `trade_batch_no` (`strategy_batch_no`),
  KEY `date_idx` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trading_strategies`
--

DROP TABLE IF EXISTS `trading_strategies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trading_strategies` (
  `pk_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(300) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT NULL,
  `trade_count` int(11) DEFAULT NULL,
  `max_earn_rate` decimal(8,2) DEFAULT NULL,
  `min_earn_rate` decimal(8,2) DEFAULT NULL,
  `avg_earn_rate` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trend_daily`
--

DROP TABLE IF EXISTS `trend_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trend_daily` (
  `pk_id` int(11) unsigned NOT NULL,
  `stock_no` varchar(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `high5` int(11) DEFAULT NULL,
  `high3` int(11) DEFAULT NULL,
  `low5` int(11) DEFAULT NULL,
  `low3` int(11) DEFAULT NULL,
  `tmrow_open_price` decimal(8,2) DEFAULT NULL,
  `price_rate_2` float DEFAULT NULL,
  `price_rate_3` float DEFAULT NULL,
  `price_rate_4` float DEFAULT NULL,
  `price_rate_5` float DEFAULT NULL,
  `history_prate_3` float DEFAULT NULL,
  `history_prate_5` float DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `stock_no` (`stock_no`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-01-03  8:58:54
