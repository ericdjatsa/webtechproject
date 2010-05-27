-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (i486)
--
-- Host: localhost    Database: playground
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12

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
-- Table structure for table `film_film`
--

DROP TABLE IF EXISTS `frontend_film`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `frontend_film` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `release_date` datetime NOT NULL,
  `image` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `film_film`
--

LOCK TABLES `frontend_film` WRITE;
/*!40000 ALTER TABLE `frontend_film` DISABLE KEYS */;
INSERT INTO `frontend_film` VALUES (1,'Mr & Mrs Smith','2005-04-26 00:00:00','http://ia.media-imdb.com/images/M/MV5BMTUxMzcxNzQzOF5BMl5BanBnXkFtZTcwMzQxNjUyMw@@._V1._SX95_SY140_.jpg'),(2,'Pirates of the Caribbean: The ','2004-12-03 00:00:00','http://ia.media-imdb.com/images/M/MV5BMjAyMDAzNTc2N15BMl5BanBnXkFtZTYwMDA4Njk5._V1._SX94_SY140_.jpg'),(8,'Le fabuleux destin d\'Amélie Po','2001-01-01 00:00:00','http://ia.media-imdb.com/images/M/MV5BMTIwODM0NzUxNl5BMl5BanBnXkFtZTcwODQxNTEzMQ@@._V1._SX100_SY133_.jpg'),(7,'Titanic','1997-01-01 00:00:00','http://ia.media-imdb.com/images/M/MV5BMTYyNzA2NzQ3Ml5BMl5BanBnXkFtZTYwNDQ1MTI5._V1._SX98_SY140_.jpg'),(6,'Avatar','2009-01-01 00:00:00','http://ia.media-imdb.com/images/M/MV5BMTA3MzcxNTI2MjNeQTJeQWpwZ15BbWU3MDYwMTc0MzM@._V1._SX100_SY122_.jpg'),(9,'Mary Poppins','1964-01-01 00:00:00','http://ia.media-imdb.com/images/M/MV5BMTgxMTcwMDE0NF5BMl5BanBnXkFtZTcwNDA4MDcyMQ@@._V1._SX100_SY140_.jpg'),(10,'Austin Powers: International M','1997-01-01 00:00:00','http://ia.media-imdb.com/images/M/MV5BMTU4MTY0NTk1MF5BMl5BanBnXkFtZTcwMjMxNTIyMQ@@._V1._SX100_SY138_.jpg'),(11,'Goldfinger','1964-01-01 00:00:00','http://ia.media-imdb.com/images/M/MV5BMTc0MDAzMDk1Ml5BMl5BanBnXkFtZTcwMjY4MDE0MQ@@._V1._SX100_SY137_.jpg');
/*!40000 ALTER TABLE `frontend_film` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-05-04 23:33:15
