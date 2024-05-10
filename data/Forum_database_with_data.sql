CREATE DATABASE  IF NOT EXISTS `forum_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `forum_app`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: forum_app
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` text DEFAULT NULL,
  `is_locked` tinyint(4) NOT NULL DEFAULT 0,
  `is_private` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Art History','All about visual art',0,0),(2,'Startups','Why we make one and how to succeed..',0,1),(3,'Interesting facts about people','Spread love not war please. Let\'s stay positive here',1,0),(4,'IT Career','Be part of a revolution',0,0);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories_access`
--

DROP TABLE IF EXISTS `categories_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories_access` (
  `categories_id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  `access_type` tinyint(4) NOT NULL DEFAULT 1,
  PRIMARY KEY (`categories_id`,`users_id`),
  KEY `fk_categories_has_users_users2_idx` (`users_id`),
  KEY `fk_categories_has_users_categories2_idx` (`categories_id`),
  CONSTRAINT `fk_categories_has_users_categories2` FOREIGN KEY (`categories_id`) REFERENCES `categories` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_categories_has_users_users2` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories_access`
--

LOCK TABLES `categories_access` WRITE;
/*!40000 ALTER TABLE `categories_access` DISABLE KEYS */;
INSERT INTO `categories_access` VALUES (2,4,0),(2,6,1),(2,7,1),(2,8,1);
/*!40000 ALTER TABLE `categories_access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `sender_id` int(11) NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`sender_id`),
  KEY `fk_messages_users2_idx` (`sender_id`),
  CONSTRAINT `fk_messages_users2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'Hi.',4,'2024-05-10 12:18:37'),(2,'Zdravey.',5,'2024-05-10 12:19:03'),(3,'asl pls',4,'2024-05-10 12:19:23'),(4,'I don\'t have time for this',5,'2024-05-10 12:19:44'),(5,'Check Google',5,'2024-05-10 12:20:10'),(6,'Just being polite. Know you are old.',4,'2024-05-10 12:20:43'),(7,'Not doing that well with it. Aye.',5,'2024-05-10 12:21:18'),(8,'Bad day?',4,'2024-05-10 12:21:31'),(9,'Anyway. Nashledanou.',5,'2024-05-10 12:23:01');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages_users`
--

DROP TABLE IF EXISTS `messages_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages_users` (
  `message_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  PRIMARY KEY (`message_id`,`receiver_id`),
  KEY `fk_messages_has_users_users1_idx` (`receiver_id`),
  KEY `fk_messages_has_users_messages1_idx` (`message_id`),
  CONSTRAINT `fk_messages_has_users_messages1` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_has_users_users1` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages_users`
--

LOCK TABLES `messages_users` WRITE;
/*!40000 ALTER TABLE `messages_users` DISABLE KEYS */;
INSERT INTO `messages_users` VALUES (2,4),(4,4),(5,4),(7,4),(9,4),(1,5),(3,5),(6,5),(8,5);
/*!40000 ALTER TABLE `messages_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `replies`
--

DROP TABLE IF EXISTS `replies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `replies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `topic_id` int(11) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`,`topic_id`),
  KEY `fk_replies_users1_idx` (`user_id`),
  KEY `fk_replies_topics1_idx` (`topic_id`),
  CONSTRAINT `fk_replies_topics1` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `replies`
--

LOCK TABLES `replies` WRITE;
/*!40000 ALTER TABLE `replies` DISABLE KEYS */;
INSERT INTO `replies` VALUES (1,1,'2024-05-09 16:57:26',1,'In my opinion, no. Da Vinci was more than just an artist. However, that said, his artistry was still over and above Van Gogh\'s, not that Vincent Van Gogh was a terrible artist. He wasn\'t.'),(2,6,'2024-05-10 09:28:05',1,'for toilet paper rolls van gogh will sell better. you know, big colorful flowers. but, da vinci wasn’t that wonderful a painter. maybe van Gogh and Giotto?DO you know Giotto'),(3,8,'2024-05-10 09:50:01',1,'What on earth do you mean by better? They lived 400 years apart, in different countries, experienced different educations, had different concepts of what it meant to create art, and had nothing in common temperamentally. The audiences for their art had little in common. Moreover, there is no metric anyone can use to arrange artists from best to worst. You, of course, can arrange your own private pantheon. You can make any judgments you want. But that\'s you.'),(4,8,'2024-05-10 09:51:59',2,'You should get into politics'),(5,2,'2024-05-10 09:52:28',2,'If you got rejected from art school, the answer is...'),(6,4,'2024-05-10 09:52:59',2,'Move On. It\'s just a college or university. Of course, it matters where you get your degree from, but you are more than just a rejection. All the best! In the long run, your skills and confidence, and capability to work smart matters.'),(7,7,'2024-05-10 10:20:15',3,'What do you mean an oil and gas venture? A traditional oil and gas play is not a startup, it’s a natural resources exploration effort. You’re investing in an oil well not a company.'),(8,6,'2024-05-10 10:21:38',3,'An oil operator drilling a single not-too-deep well on dry land finds their investors in country clubs, ranch houses, charity balls, doctor’s conventions, megachurches, chambers of commerce, winery tasting rooms, wherever you might find rich people who want to try putting money to work buying a share of a hard asset in a simple way they can understand.'),(9,7,'2024-05-10 10:23:32',4,'A startup idea is derived out of discomfort or a gap you see in the existing market. So don’t go looking here and there for that billion idea, just be more attentive and observant while looking around you, it is right there.'),(10,8,'2024-05-10 10:24:23',4,'Make sure your solution is unique, and you don\'t have a ton of competition. Use Google to search for competitors'),(11,7,'2024-05-10 10:24:59',4,'Validate demand (prove people will buy it). You can pre-sell with crowdfunding to prove this, or you can make a landing page that looks like your product is ready to go. Have your price on the landing page. When a user tries to buy capture their email, and inform them that they caught you right before launch'),(12,2,'2024-05-10 10:32:17',5,'70% of people like old songs because of the memories attached to them.'),(13,2,'2024-05-10 10:32:26',5,'When a person dies, they have 7 minutes of brain activity left, it\'s the mind playing back the person\'s memories in a dream sequence.'),(14,2,'2024-05-10 10:32:41',5,'Psychology says that playing video games makes you more creative.'),(15,2,'2024-05-10 10:36:30',5,'Most people type faster when there\'s someone they like.'),(16,6,'2024-05-10 10:36:47',5,'You appear more attractive to a person when you make them laugh or smile.'),(17,6,'2024-05-10 10:37:04',5,'80% of women choose silence to express pain. You should know she is truly hurt when she chooses to ignore you.'),(18,6,'2024-05-10 10:37:18',5,'People with sarcastic personalities are more honest with their friends.'),(19,4,'2024-05-10 10:37:38',5,'Overthinking is a special form of fear. It gets even more dangerous when anticipation, memory, emotion and imagination are added together.'),(20,4,'2024-05-10 10:37:58',5,'The average woman smiles 60 times a day. An average man smiles only 10 times a day.'),(21,4,'2024-05-10 10:38:09',5,'When people refuse to tell you what\'s wrong, you tend to think that it\'s probably your fault.'),(22,7,'2024-05-10 10:38:25',5,'Intelligent men and women are more easily annoyed by people in general.'),(23,7,'2024-05-10 10:38:37',5,'Women and men experience the same kind of emotions but women are more honest with them.'),(24,7,'2024-05-10 10:39:01',5,'Life becomes more meaningful when you understand the fact that you will not get the same moment twice in your life.'),(25,7,'2024-05-10 10:39:10',5,'What we wear tends to affect how we behave.'),(26,5,'2024-05-10 10:39:29',5,'Introverts tend to have more thinking capabilities than extroverts.'),(27,5,'2024-05-10 10:39:43',5,'Eat bananas, because bananas contain a special chemical which can make a person happy.'),(28,5,'2024-05-10 10:39:52',5,'Pretending not to care is the habit of those who care the most.'),(29,8,'2024-05-10 10:40:13',5,'Pretending not to care is the habit of those who care the most.'),(30,8,'2024-05-10 10:40:20',5,'When you become really close to someone, you can hear their voices in your head when you read their text.'),(31,8,'2024-05-10 10:40:31',5,'Being sarcastic can add upto 3 years in your life.'),(32,8,'2024-05-10 10:40:40',5,'Appreciating someone can boost their confidence and motivate them to do better things in life.'),(33,8,'2024-05-10 10:40:48',5,'Today, web development has emerged as a thriving and in-demand career choice. From building stunning websites to crafting user experiences, web development is at the forefront of shaping the online world.'),(34,6,'2024-05-10 10:47:10',6,'Today, web development has emerged as a thriving and in-demand career choice. From building stunning websites to crafting user experiences, web development is at the forefront of shaping the online world.'),(35,7,'2024-05-10 10:47:32',6,'Web development is a rewarding and promising career path with a strong job outlook and competitive salaries. The demand for skilled web developers is expected to continue growing as businesses increasingly rely on the internet to reach their target audiences.'),(36,8,'2024-05-10 10:47:47',6,'I am in web development. Great Career. Go for it.');
/*!40000 ALTER TABLE `replies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `description` text NOT NULL,
  `is_locked` tinyint(4) NOT NULL DEFAULT 0,
  `best_reply` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`,`category_id`,`user_id`),
  KEY `fk_topics_categories1_idx` (`category_id`),
  KEY `fk_topics_users1_idx` (`user_id`),
  CONSTRAINT `fk_topics_categories1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */;
INSERT INTO `topics` VALUES (1,'Was Van Gogh a better artist than Da Vinci?',1,1,'2024-05-09 16:23:35','',0,3),(2,'I just got rejected from the Academy of Fine Arts Vienna. What do I do now?',1,6,'2024-05-10 09:24:47','I recently applied to the Academy of Fine Arts Vienna, but I just received a rejection letter. I\'m feeling pretty down and unsure about my next steps. Has anyone else experienced this, and what did you do to stay motivated? I\'d appreciate any advice on other art schools or alternative paths in the art world.',0,4),(3,'How do I find a list of angel investors who specialize in oil and gas ventures?',2,8,'2024-05-10 10:17:44','',0,7),(4,'What are the best ways to think of ideas for a startup?',2,6,'2024-05-10 10:22:46','',1,9),(5,'What are the most interesting facts about human behavior?',3,2,'2024-05-10 10:31:09','',0,0),(6,'How good is web development as a career?',4,4,'2024-05-10 10:46:11','In a world of so many career, why should I choose IT?!',0,0);
/*!40000 ALTER TABLE `topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_votes`
--

DROP TABLE IF EXISTS `user_votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_votes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `vote_type` tinyint(4) NOT NULL,
  `replies_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_upvotes_users1_idx` (`user_id`),
  KEY `fk_user_votes_replies1_idx` (`replies_id`),
  CONSTRAINT `fk_upvotes_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_votes_replies1` FOREIGN KEY (`replies_id`) REFERENCES `replies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_votes`
--

LOCK TABLES `user_votes` WRITE;
/*!40000 ALTER TABLE `user_votes` DISABLE KEYS */;
INSERT INTO `user_votes` VALUES (3,4,1,2),(4,5,0,2),(5,5,1,1),(6,2,1,1),(7,2,1,3),(8,5,1,3),(9,8,1,3),(10,5,0,4),(11,7,1,4),(12,6,1,4),(13,4,0,4),(14,5,0,5),(15,4,0,6),(16,5,0,6),(17,5,0,7),(18,7,0,7),(19,5,0,8),(20,7,0,8),(21,6,1,8),(22,5,1,9),(23,7,1,9),(24,5,1,10),(25,4,0,10),(26,7,0,10),(27,8,1,10);
/*!40000 ALTER TABLE `user_votes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(200) NOT NULL,
  `role` varchar(10) NOT NULL DEFAULT 'User',
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_UNIQUE` (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','acd4b76bcf107a48b6eba829cec784c892ff9a972249f8c6bb30855d6bdca140','Admin','admin','admin','admin@admin.bg'),(2,'masteryoda','ca118e85c5b8a7ea51f7c8baa298052faa7e4c426eb4fa01c28faa08da3f672a','Admin','Master','Yoda','yoda@master.bg'),(3,'user','9b2cf83517f19be46e2067ea95f1a2151ae2892210e243988e8caa34f0423975','User','user','user','user@user.bg'),(4,'grigordimitrov','41515ac89b3a094deca69f8813f329f69da410ddb59fb861bdeaa424c6345f8b','User','Grigor','Dimitrov','grisho@top10.world'),(5,'geomilev','5b7f7c315e4d2492b133c5fe7c7ca1c19cc91cab24d693bfbc888999d3137309','User','Geo','Milev','geomilev@20century.bg'),(6,'franksinatra','205258a23ed3a772408f164a0173137378f0756651676dc3bedaade7690283c1','User','Frank','Sinatra','myway@franksinatra.com'),(7,'fionaapple','fbda9b649d12799511a0cfe48b2555209d289ab3e64c69e3d2882cf00497be11','User','Fiona','Apple','tidal@fionaapple.com'),(8,'ryanreynolds','4bf78256f15c8264984c049828805662d33e462d40943594ceef726aab74301a','User','Ryan','Reynolds','deadloop@ryanreynolds.com');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'forum_app'
--

--
-- Dumping routines for database 'forum_app'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-10 15:20:39
