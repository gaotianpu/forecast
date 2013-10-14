-- MySQL dump 10.13  Distrib 5.5.27, for osx10.6 (i386)
--
-- Host: localhost    Database: forecast
-- ------------------------------------------------------
-- Server version	5.5.27

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
  KEY `stock_no_idx` (`stock_no`),
  KEY `volume_idx` (`volume`)
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

-- Dump completed on 2013-10-14 14:03:14
