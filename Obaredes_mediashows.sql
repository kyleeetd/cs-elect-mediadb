-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: media_db
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `media_library`
--

DROP TABLE IF EXISTS `media_library`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `media_library` (
  `media_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `duration` varchar(45) DEFAULT NULL,
  `rating` varchar(45) DEFAULT NULL,
  `release_date` varchar(45) DEFAULT NULL,
  `media_type` enum('TV Show','Movie') NOT NULL,
  PRIMARY KEY (`media_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `media_library`
--

LOCK TABLES `media_library` WRITE;
/*!40000 ALTER TABLE `media_library` DISABLE KEYS */;
INSERT INTO `media_library` VALUES (1,'Stranger Things','50 min','TV-14','2016','TV Show'),(2,'The Avengers','143 min','PG-13','2012','Movie'),(3,'Breaking Bad','49 min','TV-MA','2008','TV Show'),(4,'Inception','148 min','PG-13','2010','Movie'),(5,'Game of Thrones','55 min','TV-MA','2011','TV Show'),(6,'The Dark Knight','152 min','PG-13','2008','Movie'),(7,'The Office','22 min','TV-14','2005','TV Show'),(8,'Pulp Fiction','154 min','R','1994','Movie'),(9,'Friends','22 min','TV-14','1994','TV Show'),(10,'Forrest Gump','142 min','PG-13','1994','Movie'),(11,'The Mandalorian','38 min','TV-14','2019','TV Show'),(12,'The Shawshank Redemption','142 min','R','1994','Movie'),(13,'The Crown','58 min','TV-MA','2016','TV Show'),(14,'The Godfather','175 min','R','1972','Movie'),(15,'Black Mirror','60 min','TV-MA','2011','TV Show'),(16,'Interstellar','169 min','PG-13','2014','Movie'),(17,'The Witcher','60 min','TV-MA','2019','TV Show'),(18,'Avatar','162 min','PG-13','2009','Movie'),(19,'Wednesday','45 min','TV-14','2022','TV Show'),(20,'Spider-Man: No Way Home','148 min','PG-13','2021','Movie');
/*!40000 ALTER TABLE `media_library` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `media_id` int DEFAULT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `review_text` text,
  `review_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  KEY `user_id` (`user_id`),
  KEY `media_id` (`media_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`media_id`) REFERENCES `media_library` (`media_id`),
  CONSTRAINT `reviews_chk_1` CHECK (((`rating` >= 1) and (`rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,1,3,4.5,'Amazing storyline and character development!','2023-01-15 14:30:00'),(2,2,1,5.0,'Best TV show ever made!','2023-01-20 09:15:00'),(3,3,2,4.0,'Great action scenes and visual effects.','2023-02-05 16:45:00'),(4,4,5,4.8,'Epic fantasy series with incredible world-building.','2023-02-12 11:20:00'),(5,5,6,5.0,'Heath Ledger as Joker was phenomenal!','2023-02-18 20:10:00'),(6,6,4,4.2,'Mind-bending plot with stunning visuals.','2023-03-02 13:25:00'),(7,7,7,4.7,'Hilarious and relatable workplace comedy.','2023-03-10 15:40:00'),(8,8,8,4.9,'Tarantino masterpiece! Classic cinema.','2023-03-15 18:05:00'),(9,9,9,4.6,'Timeless comedy that never gets old.','2023-03-22 10:30:00'),(10,10,10,4.3,'Heartwarming story with great performances.','2023-04-01 14:15:00'),(11,11,11,4.4,'Great Star Wars content with amazing visuals.','2023-04-08 12:50:00'),(12,12,12,5.0,'Perfect movie in every aspect.','2023-04-15 19:20:00'),(13,13,13,4.1,'Excellent historical drama with great acting.','2023-04-22 16:35:00'),(14,14,14,4.9,'The greatest film ever made.','2023-05-05 21:00:00'),(15,15,15,4.7,'Thought-provoking and often disturbing.','2023-05-12 17:45:00'),(16,16,16,4.8,'Beautiful sci-fi with emotional depth.','2023-05-20 14:10:00'),(17,17,17,4.2,'Great adaptation of the video game.','2023-05-28 11:25:00'),(18,18,18,4.0,'Visually stunning but predictable plot.','2023-06-05 15:50:00'),(19,19,19,4.5,'Fresh take on the Addams Family.','2023-06-12 13:15:00'),(20,20,20,4.6,'Best Spider-Man movie to date!','2023-06-20 18:40:00');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `join_date` date DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'john_doe','john.doe@email.com','2020-01-15'),(2,'sarah_smith','sarah.smith@email.com','2020-02-20'),(3,'mike_jones','mike.jones@email.com','2020-03-10'),(4,'emily_wilson','emily.wilson@email.com','2020-04-05'),(5,'alex_chen','alex.chen@email.com','2020-05-12'),(6,'lisa_garcia','lisa.garcia@email.com','2020-06-18'),(7,'david_brown','david.brown@email.com','2020-07-22'),(8,'amy_rodriguez','amy.rodriguez@email.com','2020-08-30'),(9,'kevin_lee','kevin.lee@email.com','2020-09-14'),(10,'jessica_taylor','jessica.taylor@email.com','2020-10-25'),(11,'ryan_martinez','ryan.martinez@email.com','2020-11-08'),(12,'megan_clark','megan.clark@email.com','2020-12-03'),(13,'chris_evans','chris.evans@email.com','2021-01-17'),(14,'olivia_parker','olivia.parker@email.com','2021-02-28'),(15,'daniel_white','daniel.white@email.com','2021-03-15'),(16,'sophia_king','sophia.king@email.com','2021-04-20'),(17,'james_scott','james.scott@email.com','2021-05-11'),(18,'emma_green','emma.green@email.com','2021-06-07'),(19,'matthew_adams','matthew.adams@email.com','2021-07-19'),(20,'ava_hall','ava.hall@email.com','2021-08-24');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-23 14:30:04
