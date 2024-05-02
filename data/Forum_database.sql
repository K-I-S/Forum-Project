CREATE DATABASE IF NOT EXISTS `forum_app`
/*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */
;
USE `forum_app`;
-- MariaDB dump 10.19-11.3.2-MariaDB, for osx10.19 (arm64)
--
-- Host: localhost    Database: forum_app
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */
;
/*!40103 SET TIME_ZONE='+00:00' */
;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */
;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */
;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */
;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */
;
--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!40101 SET character_set_client = utf8 */
;
CREATE TABLE `categories` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(45) NOT NULL,
    `description` text DEFAULT NULL,
    `is_locked` tinyint(4) NOT NULL DEFAULT 0,
    `is_private` tinyint(4) NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */
;
INSERT INTO `categories`
VALUES (
        1,
        'GoGo Penguin',
        'This is a space for all things related to this band.',
        0,
        0
    ),
    (
        2,
        'Medieval Times ',
        'All things medieval',
        0,
        0
    ),
    (3, 'Hunter x Hunter', NULL, 0, 0);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `categories_access`
--

DROP TABLE IF EXISTS `categories_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!40101 SET character_set_client = utf8 */
;
CREATE TABLE `categories_access` (
    `categories_id` int(11) NOT NULL,
    `users_id` int(11) NOT NULL,
    `access_type` tinyint(4) NOT NULL DEFAULT 1,
    PRIMARY KEY (`categories_id`, `users_id`),
    KEY `fk_categories_has_users_users2_idx` (`users_id`),
    KEY `fk_categories_has_users_categories2_idx` (`categories_id`),
    CONSTRAINT `fk_categories_has_users_categories2` FOREIGN KEY (`categories_id`) REFERENCES `categories` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `fk_categories_has_users_users2` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `categories_access`
--

LOCK TABLES `categories_access` WRITE;
/*!40000 ALTER TABLE `categories_access` DISABLE KEYS */
;
/*!40000 ALTER TABLE `categories_access` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!40101 SET character_set_client = utf8 */
;
CREATE TABLE `messages` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `text` text NOT NULL,
    `sender_id` int(11) NOT NULL,
    `date` datetime DEFAULT NULL,
    PRIMARY KEY (`id`, `sender_id`),
    KEY `fk_messages_users2_idx` (`sender_id`),
    CONSTRAINT `fk_messages_users2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */
;
/*!40000 ALTER TABLE `messages` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `messages_users`
--

DROP TABLE IF EXISTS `messages_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!40101 SET character_set_client = utf8 */
;
CREATE TABLE `messages_users` (
    `message_id` int(11) NOT NULL,
    `receiver_id` int(11) NOT NULL,
    PRIMARY KEY (`message_id`, `receiver_id`),
    KEY `fk_messages_has_users_users1_idx` (`receiver_id`),
    KEY `fk_messages_has_users_messages1_idx` (`message_id`),
    CONSTRAINT `fk_messages_has_users_messages1` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `fk_messages_has_users_users1` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `messages_users`
--

LOCK TABLES `messages_users` WRITE;
/*!40000 ALTER TABLE `messages_users` DISABLE KEYS */
;
/*!40000 ALTER TABLE `messages_users` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `replies`
--

DROP TABLE IF EXISTS `replies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!40101 SET character_set_client = utf8 */
;
CREATE TABLE `replies` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `date` datetime NOT NULL,
    `topic_id` int(11) NOT NULL,
    `content` text NOT NULL,
    PRIMARY KEY (`id`, `topic_id`),
    KEY `fk_replies_users1_idx` (`user_id`),
    KEY `fk_replies_topics1_idx` (`topic_id`),
    CONSTRAINT `fk_replies_topics1` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `fk_replies_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `replies`
--

LOCK TABLES `replies` WRITE;
/*!40000 ALTER TABLE `replies` DISABLE KEYS */
;
INSERT INTO `replies`
VALUES (
        1,
        5,
        '2024-04-25 09:49:50',
        1,
        'I am not sure. But there are rumours he is from the North Pole'
    ),
    (
        2,
        5,
        '2024-04-25 09:52:50',
        1,
        'His name is Jon Scott. He is incredibly versatile and renowed in the British jazz sphere, having spent majority of his life in London.'
    );
/*!40000 ALTER TABLE `replies` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!40101 SET character_set_client = utf8 */
;
CREATE TABLE `topics` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `title` varchar(100) NOT NULL,
    `category_id` int(11) NOT NULL,
    `user_id` int(11) NOT NULL,
    `date` datetime NOT NULL,
    `description` text NOT NULL,
    `is_locked` tinyint(4) NOT NULL DEFAULT 0,
    `best_reply` tinyint(4) NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`, `category_id`, `user_id`),
    KEY `fk_topics_categories1_idx` (`category_id`),
    KEY `fk_topics_users1_idx` (`user_id`),
    CONSTRAINT `fk_topics_categories1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `fk_topics_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */
;
INSERT INTO `topics`
VALUES (
        1,
        'Who is the new drummer?',
        1,
        3,
        '2024-04-24 15:59:12',
        'I just want to know',
        0,
        2
    ),
    (
        2,
        'Who was your favorite examiner? ',
        3,
        5,
        '2024-04-25 09:40:00',
        'I feel like each one had their own flavor, so I am curious to see different opinions.',
        0,
        0
    ),
    (
        3,
        'How old is Leorio? ',
        3,
        5,
        '2024-04-25 09:44:26',
        'He looks much older than the others.',
        0,
        0
    );
/*!40000 ALTER TABLE `topics` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `user_votes`
--

DROP TABLE IF EXISTS `user_votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!40101 SET character_set_client = utf8 */
;
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
) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `user_votes`
--

LOCK TABLES `user_votes` WRITE;
/*!40000 ALTER TABLE `user_votes` DISABLE KEYS */
;
INSERT INTO `user_votes`
VALUES (1, 2, 1, 1),
    (2, 5, 1, 2);
/*!40000 ALTER TABLE `user_votes` ENABLE KEYS */
;
UNLOCK TABLES;
--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!40101 SET character_set_client = utf8 */
;
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
) ENGINE = InnoDB AUTO_INCREMENT = 9 DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */
;
--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */
;
INSERT INTO `users`
VALUES (
        2,
        'Test_user',
        'bb4bc2cabb8a78d8ed21bbe714d323bb5fb8c2fc1f5bdd6fb8a88942dbdefba5',
        'Admin',
        'Gosho',
        'Goshev',
        'GG@abv.bg'
    ),
    (
        3,
        'Test_user2',
        'aebcd2a750d3ac5c7d1f9479fb6796beab14897d261811bbae4bc84294596e38',
        'User',
        'Gosho',
        'Goshev',
        'G1G@abv.bg'
    ),
    (
        5,
        'test_user3',
        'aebcd2a750d3ac5c7d1f9479fb6796beab14897d261811bbae4bc84294596e38',
        'Admin',
        'Gosho',
        'Goshev',
        'g1g@abv.bg'
    ),
    (
        6,
        'test_user4',
        'aebcd2a750d3ac5c7d1f9479fb6796beab14897d261811bbae4bc84294596e38',
        'User',
        'Gosho',
        'Goshev',
        'g1g@abv.bg'
    ),
    (
        7,
        'test_user5',
        'aebcd2a750d3ac5c7d1f9479fb6796beab14897d261811bbae4bc84294596e38',
        'User',
        'Gosho',
        'Goshev',
        'g1g@abv.bg'
    ),
    (
        8,
        'test_user6',
        'aebcd2a750d3ac5c7d1f9479fb6796beab14897d261811bbae4bc84294596e38',
        'User',
        'Gosho',
        'Goshev',
        'g123g@abv.bg'
    );
/*!40000 ALTER TABLE `users` ENABLE KEYS */
;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */
;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */
;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */
;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */
;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */
;
-- Dump completed on 2024-05-02 22:19:30