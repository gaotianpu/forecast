-- MySQL dump 10.13  Distrib 5.5.27, for osx10.6 (i386)
--
-- Host: localhost    Database: forecast
-- ------------------------------------------------------
-- Server version   5.5.27

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
  `price_up_percent` int(11) DEFAULT NULL,
  `volumn_up_count` int(11) DEFAULT NULL,
  `volumn_up_percent` int(11) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `date_idx` (`date`),
  KEY `plate_idx` (`plate`)
) ENGINE=InnoDB AUTO_INCREMENT=3454 DEFAULT CHARSET=utf8;
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
  `stock_no` varchar(10) DEFAULT NULL,
  `stock_name` varchar(20) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2880 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_daily_records`
--

DROP TABLE IF EXISTS `stock_daily_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_daily_records` (
  `pk_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
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
  `volume_updown_rate` decimal(7,3) DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `date_idx` (`date`),
  KEY `volume_idx` (`volume`),
  KEY `stock_no_idx` (`stock_no`)
) ENGINE=InnoDB AUTO_INCREMENT=759234 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_sums_info`
--

DROP TABLE IF EXISTS `stock_sums_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_sums_info` (
  `pk_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `stock_no` varchar(11) DEFAULT NULL,
  `max_price_2` decimal(8,2) DEFAULT NULL,
  `max_price_3` decimal(8,2) DEFAULT NULL,
  `max_price_5` decimal(8,2) DEFAULT NULL,
  `max_price_10` decimal(8,2) DEFAULT NULL,
  `max_price_15` decimal(8,2) DEFAULT NULL,
  `max_price_30` decimal(8,2) DEFAULT NULL,
  `max_price_60` decimal(8,2) DEFAULT NULL,
  `max_volumn_2` bigint(16) DEFAULT NULL,
  `max_volumn_3` bigint(16) DEFAULT NULL,
  `max_volumn_5` bigint(16) DEFAULT NULL,
  `max_volumn_10` bigint(16) DEFAULT NULL,
  `max_volumn_15` bigint(16) DEFAULT NULL,
  `max_volumn_30` bigint(16) DEFAULT NULL,
  `max_volumn_60` bigint(16) DEFAULT NULL,
  `min_price_2` decimal(8,2) DEFAULT NULL,
  `min_price_3` decimal(8,2) DEFAULT NULL,
  `min_price_5` decimal(8,2) DEFAULT NULL,
  `min_price_10` decimal(8,2) DEFAULT NULL,
  `min_price_15` decimal(8,2) DEFAULT NULL,
  `min_price_30` decimal(8,2) DEFAULT NULL,
  `min_price_60` decimal(8,2) DEFAULT NULL,
  `min_volumn_2` bigint(16) DEFAULT NULL,
  `min_volumn_3` bigint(16) DEFAULT NULL,
  `min_volumn_5` bigint(16) DEFAULT NULL,
  `min_volumn_10` bigint(16) DEFAULT NULL,
  `min_volumn_15` bigint(16) DEFAULT NULL,
  `min_volumn_30` bigint(16) DEFAULT NULL,
  `min_volumn_60` bigint(16) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  KEY `stock_no_idx` (`stock_no`)
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trading_strategies`
--

DROP TABLE IF EXISTS `trading_strategies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trading_strategies` (
  `pk_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(11) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT NULL,
  `trade_count` int(11) DEFAULT NULL,
  `max_earn_rate` decimal(8,2) DEFAULT NULL,
  `min_earn_rate` decimal(8,2) DEFAULT NULL,
  `avg_earn_rate` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-10-16 19:21:32
