-- MySQL dump 10.13  Distrib 5.1.37, for debian-linux-gnu (i486)
--
-- Host: localhost    Database: MovieDB
-- ------------------------------------------------------
-- Server version	5.1.37-1ubuntu5.1

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
-- Table structure for table `myCrawler_file`
--

DROP TABLE IF EXISTS `myCrawler_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myCrawler_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `extension` varchar(5) NOT NULL,
  `path` varchar(300) NOT NULL,
  `hash_code` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myCrawler_file`
--

LOCK TABLES `myCrawler_file` WRITE;
/*!40000 ALTER TABLE `myCrawler_file` DISABLE KEYS */;
INSERT INTO `myCrawler_file` VALUES (1,'24h.divx','.divx','Movies/Action/24h.divx','84f9ca02374d405cde203d712a962237'),(2,'Madagascar.wmv','.wmv','Movies/Cartoon/Madagascar.wmv','563804b6524c586d13fb2ab8212a34db'),(3,'Titanic.avi','.avi','Movies/Romance/Titanic.avi','ce08352067b82381694cd5c748250186'),(4,'Marimar.divx','.divx','Movies/Romance/Marimar.divx','ce39deb225ab4dccc18a17400661272a'),(5,'Avatar.avi','.avi','Movies/Action/Avatar.avi','6637b3e78dbefc3294f484cb4a7dbedf'),(6,'IronMan.wmv','.wmv','Movies/Action/IronMan.wmv','14289a7b128f860872e735a73ad322d0');
/*!40000 ALTER TABLE `myCrawler_file` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-05-02 15:46:20
