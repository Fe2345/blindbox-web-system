-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: Web
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1200000$netW4GiGUB9Qclivj8rGqd$H+vSva0vyjdPuB5QUMYsZtvAjESuEReXui54WLsYC/0=',NULL,0,'111','','','',0,1,'2026-05-29 06:12:39.981385','user','18301108746',''),(2,'pbkdf2_sha256$1200000$F4Cl1QNUsqlHrYdzFTix2H$OYAN5c5hUNy7G85rloWlTyn3NLjYUMZKGkGwIvVLDQI=',NULL,0,'testuser2','','','',0,1,'2026-05-29 06:27:28.524985','user','13800000002',''),(3,'pbkdf2_sha256$1200000$3zPsVup8qPq9LLI5XVHVyD$Clv6pjS1Q+1pqTURPSwrUxraBdNrgVxyP9awkwuCPUI=',NULL,0,'paimon','','','',0,1,'2026-06-03 07:21:03.161932','user','18301108746','/media/avatar/d5ad39290a3041a1896892812d30f655.png'),(4,'pbkdf2_sha256$1200000$VQaMwEIjM4lwVpSfOqAI0O$V8+87RS3xBAelJ3A4GyyC4N29BkjqiHVBTdyPc6JPMA=',NULL,0,'testuser','','','testuser@example.com',0,1,'2026-06-08 11:23:16.212987','user','13800000001',''),(5,'pbkdf2_sha256$1200000$aumo1lA2CT9RjMwxAkMSn6$tjhcf+/KbS/JhZsTPYYCPArr22Bvrk9+dfN+8ww1pDw=',NULL,0,'p3_exchange_user','','','p3_exchange_user@example.com',0,1,'2026-06-08 11:23:16.598051','user','13800000002',''),(6,'pbkdf2_sha256$1200000$2bST8g5nSctyCszPtO7dhZ$zYrPzn8QiZRx9Lqk3PlSR1kX4PT23amYstUsgFBBASY=',NULL,0,'p3_real_merchant','','','p3_real_merchant@example.com',0,1,'2026-06-08 11:23:16.980146','merchant','13800000003','');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add Token',7,'add_tokenproxy'),(26,'Can change Token',7,'change_tokenproxy'),(27,'Can delete Token',7,'delete_tokenproxy'),(28,'Can view Token',7,'view_tokenproxy'),(29,'Can add 鐢ㄦ埛',10,'add_user'),(30,'Can change 鐢ㄦ埛',10,'change_user'),(31,'Can delete 鐢ㄦ埛',10,'delete_user'),(32,'Can view 鐢ㄦ埛',10,'view_user'),(33,'Can add 琛屾斂鍖哄垝',9,'add_division'),(34,'Can change 琛屾斂鍖哄垝',9,'change_division'),(35,'Can delete 琛屾斂鍖哄垝',9,'delete_division'),(36,'Can view 琛屾斂鍖哄垝',9,'view_division'),(37,'Can add 鏀惰揣鍦板潃',8,'add_address'),(38,'Can change 鏀惰揣鍦板潃',8,'change_address'),(39,'Can delete 鏀惰揣鍦板潃',8,'delete_address'),(40,'Can view 鏀惰揣鍦板潃',8,'view_address'),(41,'Can add 鐩茬洅',11,'add_blindbox'),(42,'Can change 鐩茬洅',11,'change_blindbox'),(43,'Can delete 鐩茬洅',11,'delete_blindbox'),(44,'Can view 鐩茬洅',11,'view_blindbox'),(45,'Can add 濂栧搧',13,'add_prize'),(46,'Can change 濂栧搧',13,'change_prize'),(47,'Can delete 濂栧搧',13,'delete_prize'),(48,'Can view 濂栧搧',13,'view_prize'),(49,'Can add 鎶界洅璁板綍',12,'add_drawrecord'),(50,'Can change 鎶界洅璁板綍',12,'change_drawrecord'),(51,'Can delete 鎶界洅璁板綍',12,'delete_drawrecord'),(52,'Can view 鎶界洅璁板綍',12,'view_drawrecord'),(53,'Can add 鐢ㄦ埛璧勪骇',14,'add_asset'),(54,'Can change 鐢ㄦ埛璧勪骇',14,'change_asset'),(55,'Can delete 鐢ㄦ埛璧勪骇',14,'delete_asset'),(56,'Can view 鐢ㄦ埛璧勪骇',14,'view_asset'),(57,'Can add 璁㈠崟',15,'add_order'),(58,'Can change 璁㈠崟',15,'change_order'),(59,'Can delete 璁㈠崟',15,'delete_order'),(60,'Can view 璁㈠崟',15,'view_order'),(61,'Can add 鎹㈢墿甯栧瓙',17,'add_exchangepost'),(62,'Can change 鎹㈢墿甯栧瓙',17,'change_exchangepost'),(63,'Can delete 鎹㈢墿甯栧瓙',17,'delete_exchangepost'),(64,'Can view 鎹㈢墿甯栧瓙',17,'view_exchangepost'),(65,'Can add 鎹㈢墿鐢宠',16,'add_exchangeapplication'),(66,'Can change 鎹㈢墿鐢宠',16,'change_exchangeapplication'),(67,'Can delete 鎹㈢墿鐢宠',16,'delete_exchangeapplication'),(68,'Can view 鎹㈢墿鐢宠',16,'view_exchangeapplication'),(69,'Can add 绉垎璐︽埛',18,'add_pointsaccount'),(70,'Can change 绉垎璐︽埛',18,'change_pointsaccount'),(71,'Can delete 绉垎璐︽埛',18,'delete_pointsaccount'),(72,'Can view 绉垎璐︽埛',18,'view_pointsaccount'),(73,'Can add 绉垎娴佹按',19,'add_pointsrecord'),(74,'Can change 绉垎娴佹按',19,'change_pointsrecord'),(75,'Can delete 绉垎娴佹按',19,'delete_pointsrecord'),(76,'Can view 绉垎娴佹按',19,'view_pointsrecord'),(77,'Can add 浜ゆ槗璁板綍',20,'add_transactionrecord'),(78,'Can change 浜ゆ槗璁板綍',20,'change_transactionrecord'),(79,'Can delete 浜ゆ槗璁板綍',20,'delete_transactionrecord'),(80,'Can view 浜ゆ槗璁板綍',20,'view_transactionrecord'),(81,'Can add 鍟嗗',23,'add_merchant'),(82,'Can change 鍟嗗',23,'change_merchant'),(83,'Can delete 鍟嗗',23,'delete_merchant'),(84,'Can view 鍟嗗',23,'view_merchant'),(85,'Can add 鍟嗗鍟嗗搧',24,'add_product'),(86,'Can change 鍟嗗鍟嗗搧',24,'change_product'),(87,'Can delete 鍟嗗鍟嗗搧',24,'delete_product'),(88,'Can view 鍟嗗鍟嗗搧',24,'view_product'),(89,'Can add 搴撳瓨鍙樺姩璁板綍',22,'add_inventoryrecord'),(90,'Can change 搴撳瓨鍙樺姩璁板綍',22,'change_inventoryrecord'),(91,'Can delete 搴撳瓨鍙樺姩璁板綍',22,'delete_inventoryrecord'),(92,'Can view 搴撳瓨鍙樺姩璁板綍',22,'view_inventoryrecord'),(93,'Can add 搴撳瓨',21,'add_inventory'),(94,'Can change 搴撳瓨',21,'change_inventory'),(95,'Can delete 搴撳瓨',21,'delete_inventory'),(96,'Can view 搴撳瓨',21,'view_inventory'),(97,'Can add 鍙戣揣浠诲姟',25,'add_shipmenttask'),(98,'Can change 鍙戣揣浠诲姟',25,'change_shipmenttask'),(99,'Can delete 鍙戣揣浠诲姟',25,'delete_shipmenttask'),(100,'Can view 鍙戣揣浠诲姟',25,'view_shipmenttask'),(101,'Can add 寮傚父宸ュ崟',26,'add_exceptionrecord'),(102,'Can change 寮傚父宸ュ崟',26,'change_exceptionrecord'),(103,'Can delete 寮傚父宸ュ崟',26,'delete_exceptionrecord'),(104,'Can view 寮傚父宸ュ崟',26,'view_exceptionrecord'),(105,'Can add 鎿嶄綔鏃ュ織',27,'add_oplog'),(106,'Can change 鎿嶄綔鏃ュ織',27,'change_oplog'),(107,'Can delete 鎿嶄綔鏃ュ織',27,'delete_oplog'),(108,'Can view 鎿嶄綔鏃ュ織',27,'view_oplog'),(109,'Can add 瑙勫垯閰嶇疆',28,'add_ruleconfig'),(110,'Can change 瑙勫垯閰嶇疆',28,'change_ruleconfig'),(111,'Can delete 瑙勫垯閰嶇疆',28,'delete_ruleconfig'),(112,'Can view 瑙勫垯閰嶇疆',28,'view_ruleconfig'),(113,'Can add 浜ゆ槗璐︽湰',29,'add_transactionledger'),(114,'Can change 浜ゆ槗璐︽湰',29,'change_transactionledger'),(115,'Can delete 浜ゆ槗璐︽湰',29,'delete_transactionledger'),(116,'Can view 浜ゆ槗璐︽湰',29,'view_transactionledger');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blindbox`
--

DROP TABLE IF EXISTS `blindbox`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blindbox` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cover` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cost_points` int unsigned NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `ip_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `max_draw_count` int unsigned NOT NULL,
  `allow_simulation` tinyint(1) NOT NULL,
  `sort_order` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `blindbox_chk_1` CHECK ((`cost_points` >= 0)),
  CONSTRAINT `blindbox_chk_2` CHECK ((`max_draw_count` >= 0)),
  CONSTRAINT `blindbox_chk_3` CHECK ((`sort_order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blindbox`
--

LOCK TABLES `blindbox` WRITE;
/*!40000 ALTER TABLE `blindbox` DISABLE KEYS */;
INSERT INTO `blindbox` VALUES (1,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830','P3真实EVA主题盲盒','/media/product/EVA 机体设定海报.png','P3_REAL 基于真实图片生成的EVA测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','EVA',10,1,1),(2,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830','P3真实Fate主题盲盒','/media/product/Saber誓约胜利之剑手办.png','P3_REAL 基于真实图片生成的Fate测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','Fate',10,1,2),(3,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830','P3真实JOJO主题盲盒','/media/product/乔鲁诺黄金体验徽章.png','P3_REAL 基于真实图片生成的JOJO测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','JOJO',10,1,3),(4,'2026-06-08 11:23:17.448197','2026-06-08 11:23:17.448197','P3真实原神主题盲盒','/media/product/枫原万叶流沙亚克力.png','P3_REAL 基于真实图片生成的原神测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','原神',10,1,4),(5,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834','P3真实咒术回战主题盲盒','/media/product/五条悟无量空处手办.png','P3_REAL 基于真实图片生成的咒术回战测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','咒术回战',10,1,5),(6,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834','P3真实宝可梦主题盲盒','/media/product/丰缘三神.png','P3_REAL 基于真实图片生成的宝可梦测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','宝可梦',10,1,6),(7,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834','P3真实明日方舟主题盲盒','/media/product/凯尔希女仆亚克力立牌.png','P3_REAL 基于真实图片生成的明日方舟测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','明日方舟',10,1,7),(8,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928','P3真实海贼王主题盲盒','/media/product/乔巴冬岛毛绒玩偶.png','P3_REAL 基于真实图片生成的海贼王测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','海贼王',10,1,8),(9,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928','P3真实综合动漫主题盲盒','/media/product/亚丝娜亚克力挂件.png','P3_REAL 基于真实图片生成的综合动漫测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',80,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','综合动漫',10,1,9),(10,'2026-06-08 11:23:17.465501','2026-06-08 11:23:17.465501','P3真实鬼灭之刃主题盲盒','/media/product/嘴平伊之助毛绒挂件.png','P3_REAL 基于真实图片生成的鬼灭之刃测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','鬼灭之刃',10,1,10),(11,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009','P3真实黑白的阿维斯塔主题盲盒','/media/product/《黑白的阿维斯塔》小说第一卷 凶战士篇.jpg','P3_REAL 基于真实图片生成的黑白的阿维斯塔测试盲盒，支持单抽、五连抽、十连抽和结果回收。','IP主题盲盒',100,'active','2026-06-07 11:23:17.440830','2026-09-06 11:23:17.440830','黑白的阿维斯塔',10,1,11);
/*!40000 ALTER TABLE `blindbox` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blindbox_draw_record`
--

DROP TABLE IF EXISTS `blindbox_draw_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blindbox_draw_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `prize_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prize_image` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rarity` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cost_points` int unsigned NOT NULL,
  `blindbox_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `prize_id` bigint NOT NULL,
  `asset_id` bigint DEFAULT NULL,
  `remaining_points` int unsigned NOT NULL,
  `batch_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `draw_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `draw_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_name_snapshot` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blindbox_draw_record_blindbox_id_1e60d661_fk_blindbox_id` (`blindbox_id`),
  KEY `blindbox_draw_record_user_id_097d3e33_fk_accounts_user_id` (`user_id`),
  KEY `blindbox_draw_record_prize_id_7005b646_fk_blindbox_prize_id` (`prize_id`),
  KEY `blindbox_draw_record_asset_id_4d66644d_fk_user_asset_id` (`asset_id`),
  CONSTRAINT `blindbox_draw_record_asset_id_4d66644d_fk_user_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `user_asset` (`id`),
  CONSTRAINT `blindbox_draw_record_blindbox_id_1e60d661_fk_blindbox_id` FOREIGN KEY (`blindbox_id`) REFERENCES `blindbox` (`id`),
  CONSTRAINT `blindbox_draw_record_prize_id_7005b646_fk_blindbox_prize_id` FOREIGN KEY (`prize_id`) REFERENCES `blindbox_prize` (`id`),
  CONSTRAINT `blindbox_draw_record_user_id_097d3e33_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `blindbox_draw_record_chk_1` CHECK ((`cost_points` >= 0)),
  CONSTRAINT `blindbox_draw_record_chk_2` CHECK ((`remaining_points` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blindbox_draw_record`
--

LOCK TABLES `blindbox_draw_record` WRITE;
/*!40000 ALTER TABLE `blindbox_draw_record` DISABLE KEYS */;
INSERT INTO `blindbox_draw_record` VALUES (1,'2026-06-08 11:27:24.496177','2026-06-08 11:27:24.496177','明日香红色驾驶服手办','/media/product/明日香红色驾驶服手办.png','SSR',100,1,4,3,65,9000,'B20260608112724EC017E','real','success','EVA'),(2,'2026-06-08 11:27:24.498719','2026-06-08 11:27:24.498719','明日香限定卡片','/media/product/明日香限定卡片.png','SR',100,1,4,4,66,9000,'B20260608112724EC017E','real','success','EVA'),(3,'2026-06-08 11:27:24.502230','2026-06-08 11:27:24.502230','明日香限定卡片','/media/product/明日香限定卡片.png','SR',100,1,4,4,67,9000,'B20260608112724EC017E','real','success','EVA'),(4,'2026-06-08 11:27:24.502230','2026-06-08 11:27:24.502230','明日香限定卡片','/media/product/明日香限定卡片.png','SR',100,1,4,4,68,9000,'B20260608112724EC017E','real','success','EVA'),(5,'2026-06-08 11:27:24.508873','2026-06-08 11:27:24.508873','初号机金属徽章','/media/product/初号机金属徽章.png','SR',100,1,4,2,69,9000,'B20260608112724EC017E','real','success','EVA'),(6,'2026-06-08 11:27:24.512871','2026-06-08 11:27:24.512871','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','R',100,1,4,1,70,9000,'B20260608112724EC017E','real','success','EVA'),(7,'2026-06-08 11:27:24.516496','2026-06-08 11:27:24.516496','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','R',100,1,4,1,71,9000,'B20260608112724EC017E','real','success','EVA'),(8,'2026-06-08 11:27:24.519502','2026-06-08 11:27:24.519502','绫波丽白色驾驶服手办','/media/product/绫波丽白色驾驶服手办.png','SSR',100,1,4,5,72,9000,'B20260608112724EC017E','real','success','EVA'),(9,'2026-06-08 11:27:24.522283','2026-06-08 11:27:24.522283','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','R',100,1,4,1,73,9000,'B20260608112724EC017E','real','success','EVA'),(10,'2026-06-08 11:27:24.525030','2026-06-08 11:27:24.525030','绫波丽白色驾驶服手办','/media/product/绫波丽白色驾驶服手办.png','SSR',100,1,4,5,74,9000,'B20260608112724EC017E','real','success','EVA');
/*!40000 ALTER TABLE `blindbox_draw_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blindbox_prize`
--

DROP TABLE IF EXISTS `blindbox_prize`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blindbox_prize` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rarity` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `probability` int unsigned NOT NULL,
  `blindbox_id` bigint NOT NULL,
  `product_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `weight` int unsigned NOT NULL,
  `quantity` int unsigned NOT NULL,
  `remaining_quantity` int unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `ip_name_snapshot` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blindbox_prize_blindbox_id_3eadd5e0_fk_blindbox_id` (`blindbox_id`),
  KEY `blindbox_prize_product_id_91bf9425_fk_merchant_product_id` (`product_id`),
  CONSTRAINT `blindbox_prize_blindbox_id_3eadd5e0_fk_blindbox_id` FOREIGN KEY (`blindbox_id`) REFERENCES `blindbox` (`id`),
  CONSTRAINT `blindbox_prize_product_id_91bf9425_fk_merchant_product_id` FOREIGN KEY (`product_id`) REFERENCES `merchant_product` (`id`),
  CONSTRAINT `blindbox_prize_chk_1` CHECK ((`probability` >= 0)),
  CONSTRAINT `blindbox_prize_chk_3` CHECK ((`weight` >= 0)),
  CONSTRAINT `blindbox_prize_chk_4` CHECK ((`quantity` >= 0)),
  CONSTRAINT `blindbox_prize_chk_5` CHECK ((`remaining_quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blindbox_prize`
--

LOCK TABLES `blindbox_prize` WRITE;
/*!40000 ALTER TABLE `blindbox_prize` DISABLE KEYS */;
INSERT INTO `blindbox_prize` VALUES (1,'EVA 机体设定海报','/media/product/EVA 机体设定海报.png','R',20,1,1,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',20,35,32,1,'EVA'),(2,'初号机金属徽章','/media/product/初号机金属徽章.png','SR',20,1,16,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',20,35,34,1,'EVA'),(3,'明日香红色驾驶服手办','/media/product/明日香红色驾驶服手办.png','SSR',20,1,33,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',20,35,34,1,'EVA'),(4,'明日香限定卡片','/media/product/明日香限定卡片.png','SR',20,1,34,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',20,35,32,1,'EVA'),(5,'绫波丽白色驾驶服手办','/media/product/绫波丽白色驾驶服手办.png','SSR',20,1,56,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',20,35,33,1,'EVA'),(6,'Saber誓约胜利之剑手办','/media/product/Saber誓约胜利之剑手办.png','SSR',34,2,2,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',34,35,35,1,'Fate'),(7,'远坂凛宝石魔术徽章','/media/product/远坂凛宝石魔术徽章.png','N',33,2,67,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',33,35,35,1,'Fate'),(8,'间桐樱樱花亚克力','/media/product/间桐樱樱花亚克力.png','SR',33,2,71,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',33,35,35,1,'Fate'),(9,'乔鲁诺黄金体验徽章','/media/product/乔鲁诺黄金体验徽章.png','N',50,3,9,'2026-06-08 11:23:17.448197','2026-06-08 11:23:17.448197',50,35,35,1,'JOJO'),(10,'空条承太郎白金之星手办','/media/product/空条承太郎白金之星手办.png','SSR',50,3,52,'2026-06-08 11:23:17.448197','2026-06-08 11:23:17.448197',50,35,35,1,'JOJO'),(11,'枫原万叶流沙亚克力','/media/product/枫原万叶流沙亚克力.png','SR',20,4,38,'2026-06-08 11:23:17.448197','2026-06-08 11:23:17.448197',20,35,35,1,'原神'),(12,'纳西妲立牌','/media/product/纳西妲立牌.png','SR',20,4,55,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'原神'),(13,'芙宁娜纪念卡册','/media/product/芙宁娜纪念卡册.png','R',20,4,59,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'原神'),(14,'钟离烫金色纸','/media/product/钟离烫金色纸.png','SSR',20,4,69,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'原神'),(15,'雷电影主题徽章套装','/media/product/雷电影主题徽章套装.png','SSR',20,4,76,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'原神'),(16,'五条悟无量空处手办','/media/product/五条悟无量空处手办.png','SSR',25,5,10,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',25,35,35,1,'咒术回战'),(17,'伏黑惠海报','/media/product/伏黑惠海报.png','R',25,5,12,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',25,35,35,1,'咒术回战'),(18,'虎杖悠仁战斗徽章','/media/product/虎杖悠仁战斗徽章.png','N',25,5,62,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',25,35,35,1,'咒术回战'),(19,'钉崎野蔷薇亚克力挂件','/media/product/钉崎野蔷薇亚克力挂件.png','SR',25,5,68,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',25,35,35,1,'咒术回战'),(20,'丰缘三神','/media/product/丰缘三神.png','SR',20,6,7,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'宝可梦'),(21,'沙奈朵手办','/media/product/沙奈朵手办.png','SSR',20,6,40,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'宝可梦'),(22,'皮卡丘毛绒玩偶','/media/product/皮卡丘毛绒玩偶.png','R',20,6,50,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'宝可梦'),(23,'超梦手办','/media/product/超梦手办.png','SSR',20,6,64,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'宝可梦'),(24,'骑拉帝纳','/media/product/骑拉帝纳.png','SSR',20,6,77,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',20,35,35,1,'宝可梦'),(25,'凯尔希女仆亚克力立牌','/media/product/凯尔希女仆亚克力立牌.png','SR',13,7,15,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',13,35,35,1,'明日方舟'),(26,'史尔特尔主题立牌','/media/product/史尔特尔主题立牌.png','SR',13,7,20,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',13,35,35,1,'明日方舟'),(27,'森蚺手办','/media/product/森蚺手办.png','SSR',13,7,39,'2026-06-08 11:23:17.449834','2026-06-08 11:23:17.449834',13,35,35,1,'明日方舟'),(28,'浊心斯卡蒂深海主题徽章','/media/product/浊心斯卡蒂深海主题徽章.png','N',13,7,42,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',13,35,35,1,'明日方舟'),(29,'能天使拉特兰亚克力立牌','/media/product/能天使拉特兰亚克力立牌.png','SR',12,7,57,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',12,35,35,1,'明日方舟'),(30,'艾雅法拉手办','/media/product/艾雅法拉手办.png','SSR',12,7,58,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',12,35,35,1,'明日方舟'),(31,'银灰谢拉格收藏立牌','/media/product/银灰谢拉格收藏立牌.png','SR',12,7,70,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',12,35,35,1,'明日方舟'),(32,'阿米娅罗德岛徽章','/media/product/阿米娅罗德岛徽章.png','N',12,7,74,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',12,35,35,1,'明日方舟'),(33,'乔巴冬岛毛绒玩偶','/media/product/乔巴冬岛毛绒玩偶.png','R',20,8,8,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',20,35,35,1,'海贼王'),(34,'娜美航海图卡套','/media/product/娜美航海图卡套.png','N',20,8,25,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',20,35,35,1,'海贼王'),(35,'索隆三刀流亚克力','/media/product/索隆三刀流亚克力.png','SR',20,8,53,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',20,35,35,1,'海贼王'),(36,'路飞五档海报','/media/product/路飞五档海报.png','R',20,8,65,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',20,35,35,1,'海贼王'),(37,'路飞尼卡手办','/media/product/路飞尼卡手办.png','SSR',20,8,66,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',20,35,35,1,'海贼王'),(38,'亚丝娜亚克力挂件','/media/product/亚丝娜亚克力挂件.png','SR',13,9,11,'2026-06-08 11:23:17.457928','2026-06-08 11:23:17.457928',13,35,35,1,'综合动漫'),(39,'佐助须佐能乎徽章','/media/product/佐助须佐能乎徽章.png','N',13,9,13,'2026-06-08 11:23:17.462987','2026-06-08 11:23:17.462987',13,35,35,1,'综合动漫'),(40,'冈部伦太郎凤凰院徽章','/media/product/冈部伦太郎凤凰院徽章.png','N',13,9,14,'2026-06-08 11:23:17.462987','2026-06-08 11:23:17.462987',13,35,35,1,'综合动漫'),(41,'初音未来雪未来手办','/media/product/初音未来雪未来手办.png','SSR',13,9,17,'2026-06-08 11:23:17.462987','2026-06-08 11:23:17.462987',13,35,35,1,'综合动漫'),(42,'劳埃德任务卡片','/media/product/劳埃德任务卡片.png','N',12,9,18,'2026-06-08 11:23:17.462987','2026-06-08 11:23:17.462987',12,35,35,1,'综合动漫'),(43,'卡卡西写轮眼海报','/media/product/卡卡西写轮眼海报.png','R',12,9,19,'2026-06-08 11:23:17.462987','2026-06-08 11:23:17.462987',12,35,35,1,'综合动漫'),(44,'喜多川海梦水族馆立牌','/media/product/喜多川海梦水族馆立牌.png','SR',12,9,21,'2026-06-08 11:23:17.462987','2026-06-08 11:23:17.462987',12,35,35,1,'综合动漫'),(45,'夜刀神十香灵装徽章','/media/product/夜刀神十香灵装徽章.png','N',12,9,23,'2026-06-08 11:23:17.462987','2026-06-08 11:23:17.462987',12,35,35,1,'综合动漫'),(46,'嘴平伊之助毛绒挂件','/media/product/嘴平伊之助毛绒挂件.png','R',17,10,22,'2026-06-08 11:23:17.465501','2026-06-08 11:23:17.465501',17,35,35,1,'鬼灭之刃'),(47,'我妻善逸雷之呼吸徽章','/media/product/我妻善逸雷之呼吸徽章.png','N',17,10,28,'2026-06-08 11:23:17.465501','2026-06-08 11:23:17.465501',17,35,35,1,'鬼灭之刃'),(48,'灶门炭治郎水之呼吸手办','/media/product/灶门炭治郎水之呼吸手办.png','SSR',17,10,44,'2026-06-08 11:23:17.465501','2026-06-08 11:23:17.465501',17,35,35,1,'鬼灭之刃'),(49,'炭治郎日轮刀模型','/media/product/炭治郎日轮刀模型.png','SSR',17,10,45,'2026-06-08 11:23:17.465501','2026-06-08 11:23:17.465501',17,35,35,1,'鬼灭之刃'),(50,'祢豆子竹筒玩偶','/media/product/祢豆子竹筒玩偶.png','R',16,10,51,'2026-06-08 11:23:17.465501','2026-06-08 11:23:17.468009',16,35,35,1,'鬼灭之刃'),(51,'蝴蝶忍色纸','/media/product/蝴蝶忍色纸.png','SR',16,10,63,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009',16,35,35,1,'鬼灭之刃'),(52,'《黑白的阿维斯塔》小说第一卷 凶战士篇','/media/product/《黑白的阿维斯塔》小说第一卷 凶战士篇.jpg','R',25,11,3,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009',25,35,35,1,'黑白的阿维斯塔'),(53,'《黑白的阿维斯塔》小说第三卷 不变之物篇','/media/product/《黑白的阿维斯塔》小说第三卷 不变之物篇.jpg','R',25,11,4,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009',25,35,35,1,'黑白的阿维斯塔'),(54,'《黑白的阿维斯塔》小说第二卷 惭愧之空篇','/media/product/《黑白的阿维斯塔》小说第二卷 惭愧之空篇.jpg','R',25,11,5,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009',25,35,35,1,'黑白的阿维斯塔'),(55,'《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇','/media/product/《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇.jpg','R',25,11,6,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009',25,35,35,1,'黑白的阿维斯塔');
/*!40000 ALTER TABLE `blindbox_prize` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `division`
--

DROP TABLE IF EXISTS `division`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `division` (
  `code` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `level` smallint NOT NULL,
  `parent_id` varchar(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`code`),
  KEY `division_parent_id_eaaa544e_fk_division_code` (`parent_id`),
  CONSTRAINT `division_parent_id_eaaa544e_fk_division_code` FOREIGN KEY (`parent_id`) REFERENCES `division` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `division`
--

LOCK TABLES `division` WRITE;
/*!40000 ALTER TABLE `division` DISABLE KEYS */;
/*!40000 ALTER TABLE `division` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'accounts','address'),(9,'accounts','division'),(10,'accounts','user'),(1,'admin','logentry'),(14,'assets','asset'),(2,'auth','group'),(3,'auth','permission'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(11,'blindbox','blindbox'),(12,'blindbox','drawrecord'),(13,'blindbox','prize'),(4,'contenttypes','contenttype'),(16,'exchange','exchangeapplication'),(17,'exchange','exchangepost'),(21,'merchant','inventory'),(22,'merchant','inventoryrecord'),(23,'merchant','merchant'),(24,'merchant','product'),(25,'merchant','shipmenttask'),(26,'operations','exceptionrecord'),(27,'operations','oplog'),(28,'operations','ruleconfig'),(29,'operations','transactionledger'),(15,'orders','order'),(18,'points','pointsaccount'),(19,'points','pointsrecord'),(20,'points','transactionrecord'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-05-29 01:25:18.224911'),(2,'contenttypes','0002_remove_content_type_name','2026-05-29 01:25:18.255961'),(3,'auth','0001_initial','2026-05-29 01:25:18.333023'),(4,'auth','0002_alter_permission_name_max_length','2026-05-29 01:25:18.347601'),(5,'auth','0003_alter_user_email_max_length','2026-05-29 01:25:18.350296'),(6,'auth','0004_alter_user_username_opts','2026-05-29 01:25:18.352660'),(7,'auth','0005_alter_user_last_login_null','2026-05-29 01:25:18.355015'),(8,'auth','0006_require_contenttypes_0002','2026-05-29 01:25:18.356263'),(9,'auth','0007_alter_validators_add_error_messages','2026-05-29 01:25:18.358335'),(10,'auth','0008_alter_user_username_max_length','2026-05-29 01:25:18.360519'),(11,'auth','0009_alter_user_last_name_max_length','2026-05-29 01:25:18.363124'),(12,'auth','0010_alter_group_name_max_length','2026-05-29 01:25:18.372109'),(13,'auth','0011_update_proxy_permissions','2026-05-29 01:25:18.376072'),(14,'auth','0012_alter_user_first_name_max_length','2026-05-29 01:25:18.378388'),(15,'accounts','0001_initial','2026-05-29 01:25:18.583948'),(16,'admin','0001_initial','2026-05-29 01:25:18.621404'),(17,'admin','0002_logentry_remove_auto_add','2026-05-29 01:25:18.625078'),(18,'admin','0003_logentry_add_action_flag_choices','2026-05-29 01:25:18.629380'),(19,'merchant','0001_initial','2026-05-29 01:25:18.752570'),(20,'blindbox','0001_initial','2026-05-29 01:25:18.851164'),(21,'assets','0001_initial','2026-05-29 01:25:18.906498'),(22,'authtoken','0001_initial','2026-05-29 01:25:18.932250'),(23,'authtoken','0002_auto_20160226_1747','2026-05-29 01:25:18.949375'),(24,'authtoken','0003_tokenproxy','2026-05-29 01:25:18.951579'),(25,'authtoken','0004_alter_tokenproxy_options','2026-05-29 01:25:18.954323'),(26,'exchange','0001_initial','2026-05-29 01:25:19.047033'),(27,'operations','0001_initial','2026-05-29 01:25:19.069220'),(28,'orders','0001_initial','2026-05-29 01:25:19.113143'),(29,'points','0001_initial','2026-05-29 01:25:19.190351'),(30,'sessions','0001_initial','2026-05-29 01:25:19.206842'),(31,'blindbox','0002_update_blindbox_prize_drawrecord','2026-06-01 13:56:13.921672');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exception_record`
--

DROP TABLE IF EXISTS `exception_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exception_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `related_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `result` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `resolved_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exception_record`
--

LOCK TABLES `exception_record` WRITE;
/*!40000 ALTER TABLE `exception_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `exception_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_application`
--

DROP TABLE IF EXISTS `exchange_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchange_application` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `applicant_asset_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applicant_asset_image` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applicant_asset_rarity` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_asset_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_asset_image` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `post_asset_rarity` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `remark` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applicant_id` bigint NOT NULL,
  `applicant_asset_id` bigint NOT NULL,
  `post_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchange_application_applicant_id_40020fdc_fk_accounts_user_id` (`applicant_id`),
  KEY `exchange_application_applicant_asset_id_e7717d56_fk_user_asse` (`applicant_asset_id`),
  KEY `exchange_application_post_id_f09f90e7_fk_exchange_post_id` (`post_id`),
  CONSTRAINT `exchange_application_applicant_asset_id_e7717d56_fk_user_asse` FOREIGN KEY (`applicant_asset_id`) REFERENCES `user_asset` (`id`),
  CONSTRAINT `exchange_application_applicant_id_40020fdc_fk_accounts_user_id` FOREIGN KEY (`applicant_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `exchange_application_post_id_f09f90e7_fk_exchange_post_id` FOREIGN KEY (`post_id`) REFERENCES `exchange_post` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_application`
--

LOCK TABLES `exchange_application` WRITE;
/*!40000 ALTER TABLE `exchange_application` DISABLE KEYS */;
INSERT INTO `exchange_application` VALUES (1,'2026-06-08 11:23:17.507964','2026-06-08 11:23:17.507964','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','R','灶门炭治郎水之呼吸手办','/media/product/灶门炭治郎水之呼吸手办.png','SSR','P3_REAL pending application','pending',4,1,8);
/*!40000 ALTER TABLE `exchange_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchange_post`
--

DROP TABLE IF EXISTS `exchange_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchange_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `asset_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `asset_image` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `asset_rarity` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `asset_category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expect_description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `remark` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `asset_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchange_post_asset_id_389298cd_fk_user_asset_id` (`asset_id`),
  KEY `exchange_post_user_id_f9853589_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `exchange_post_asset_id_389298cd_fk_user_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `user_asset` (`id`),
  CONSTRAINT `exchange_post_user_id_f9853589_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_post`
--

LOCK TABLES `exchange_post` WRITE;
/*!40000 ALTER TABLE `exchange_post` DISABLE KEYS */;
INSERT INTO `exchange_post` VALUES (1,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','有马加奈角色立牌','/media/product/有马加奈角色立牌.png','SR','亚克力','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 1','published',45,5),(2,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','枫原万叶流沙亚克力','/media/product/枫原万叶流沙亚克力.png','SR','亚克力','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 2','published',46,5),(3,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','森蚺手办','/media/product/森蚺手办.png','SSR','手办','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 3','published',47,5),(4,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','沙奈朵手办','/media/product/沙奈朵手办.png','SSR','手办','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 4','published',48,5),(5,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','波奇塔毛绒挂件','/media/product/波奇塔毛绒挂件.png','R','毛绒','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 5','published',49,5),(6,'2026-06-08 11:23:17.504480','2026-06-08 11:23:17.504480','浊心斯卡蒂深海主题徽章','/media/product/浊心斯卡蒂深海主题徽章.png','N','徽章','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 6','published',50,5),(7,'2026-06-08 11:23:17.504480','2026-06-08 11:23:17.504480','火陈通行证挂件','/media/product/火陈通行证挂件.png','N','挂件','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 7','published',51,5),(8,'2026-06-08 11:23:17.507964','2026-06-08 11:23:17.507964','灶门炭治郎水之呼吸手办','/media/product/灶门炭治郎水之呼吸手办.png','SSR','手办','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 8','published',52,5),(9,'2026-06-08 11:23:17.507964','2026-06-08 11:23:17.507964','炭治郎日轮刀模型','/media/product/炭治郎日轮刀模型.png','SSR','手办','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 9','published',53,5),(10,'2026-06-08 11:23:17.507964','2026-06-08 11:23:17.507964','爱蜜莉雅雪花手办','/media/product/爱蜜莉雅雪花手办.png','SSR','手办','希望交换同IP角色、SSR/SR手办、亚克力立牌或稀有徽章。','P3_REAL published exchange post 10','published',54,5);
/*!40000 ALTER TABLE `exchange_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merchant`
--

DROP TABLE IF EXISTS `merchant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `license` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `business_scope` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `supply_desc` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `credit_score` int NOT NULL,
  `review_note` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `merchant_user_id_8b73be38_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant`
--

LOCK TABLES `merchant` WRITE;
/*!40000 ALTER TABLE `merchant` DISABLE KEYS */;
INSERT INTO `merchant` VALUES (1,'2026-06-08 11:23:17.333119','2026-06-08 11:23:17.333119','P3真实测试商家','P3测试负责人','13800000003','p3_real_merchant@example.com','P3-REAL-SEED','动漫IP周边、盲盒奖品、换物测试商品','P3_REAL 由本地真实图片生成','approved',100,'P3_REAL 自动审核通过','2026-06-08 11:23:17.333119',6);
/*!40000 ALTER TABLE `merchant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merchant_inventory`
--

DROP TABLE IF EXISTS `merchant_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchant_inventory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `current_stock` int unsigned NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`),
  CONSTRAINT `merchant_inventory_product_id_3dd11448_fk_merchant_product_id` FOREIGN KEY (`product_id`) REFERENCES `merchant_product` (`id`),
  CONSTRAINT `merchant_inventory_chk_1` CHECK ((`current_stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant_inventory`
--

LOCK TABLES `merchant_inventory` WRITE;
/*!40000 ALTER TABLE `merchant_inventory` DISABLE KEYS */;
INSERT INTO `merchant_inventory` VALUES (1,'2026-06-08 11:23:17.349514','2026-06-08 11:23:17.350511',50,1),(2,'2026-06-08 11:23:17.352511','2026-06-08 11:23:17.352511',50,2),(3,'2026-06-08 11:23:17.353517','2026-06-08 11:23:17.353517',50,3),(4,'2026-06-08 11:23:17.354518','2026-06-08 11:23:17.354518',50,4),(5,'2026-06-08 11:23:17.355550','2026-06-08 11:23:17.355550',50,5),(6,'2026-06-08 11:23:17.356515','2026-06-08 11:23:17.356515',50,6),(7,'2026-06-08 11:23:17.358045','2026-06-08 11:23:17.358045',50,7),(8,'2026-06-08 11:23:17.359067','2026-06-08 11:23:17.359067',50,8),(9,'2026-06-08 11:23:17.360068','2026-06-08 11:23:17.360068',50,9),(10,'2026-06-08 11:23:17.361068','2026-06-08 11:23:17.361068',50,10),(11,'2026-06-08 11:23:17.362092','2026-06-08 11:23:17.362092',50,11),(12,'2026-06-08 11:23:17.362092','2026-06-08 11:23:17.362092',50,12),(13,'2026-06-08 11:23:17.365073','2026-06-08 11:23:17.365073',50,13),(14,'2026-06-08 11:23:17.365073','2026-06-08 11:23:17.365073',50,14),(15,'2026-06-08 11:23:17.365073','2026-06-08 11:23:17.365073',50,15),(16,'2026-06-08 11:23:17.368074','2026-06-08 11:23:17.368074',50,16),(17,'2026-06-08 11:23:17.368074','2026-06-08 11:23:17.368074',50,17),(18,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079',50,18),(19,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079',50,19),(20,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079',50,20),(21,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079',50,21),(22,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079',50,22),(23,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079',50,23),(24,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199',50,24),(25,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199',50,25),(26,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199',50,26),(27,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199',50,27),(28,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199',50,28),(29,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236',50,29),(30,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236',50,30),(31,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236',50,31),(32,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236',50,32),(33,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236',50,33),(34,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258',50,34),(35,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258',50,35),(36,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258',50,36),(37,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258',50,37),(38,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815',50,38),(39,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815',50,39),(40,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815',50,40),(41,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815',50,41),(42,'2026-06-08 11:23:17.396831','2026-06-08 11:23:17.396831',50,42),(43,'2026-06-08 11:23:17.397868','2026-06-08 11:23:17.397868',50,43),(44,'2026-06-08 11:23:17.399380','2026-06-08 11:23:17.399380',50,44),(45,'2026-06-08 11:23:17.400338','2026-06-08 11:23:17.400338',50,45),(46,'2026-06-08 11:23:17.402637','2026-06-08 11:23:17.402637',50,46),(47,'2026-06-08 11:23:17.403637','2026-06-08 11:23:17.403637',50,47),(48,'2026-06-08 11:23:17.404652','2026-06-08 11:23:17.404652',50,48),(49,'2026-06-08 11:23:17.405755','2026-06-08 11:23:17.405755',50,49),(50,'2026-06-08 11:23:17.407492','2026-06-08 11:23:17.407492',50,50),(51,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810',50,51),(52,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810',50,52),(53,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810',50,53),(54,'2026-06-08 11:23:17.413275','2026-06-08 11:23:17.413275',50,54),(55,'2026-06-08 11:23:17.414509','2026-06-08 11:23:17.414509',50,55),(56,'2026-06-08 11:23:17.416506','2026-06-08 11:23:17.416506',50,56),(57,'2026-06-08 11:23:17.416506','2026-06-08 11:23:17.416506',50,57),(58,'2026-06-08 11:23:17.418034','2026-06-08 11:23:17.418034',50,58),(59,'2026-06-08 11:23:17.419053','2026-06-08 11:23:17.419053',50,59),(60,'2026-06-08 11:23:17.420056','2026-06-08 11:23:17.420056',50,60),(61,'2026-06-08 11:23:17.422051','2026-06-08 11:23:17.422051',50,61),(62,'2026-06-08 11:23:17.423070','2026-06-08 11:23:17.423070',50,62),(63,'2026-06-08 11:23:17.424056','2026-06-08 11:23:17.424056',50,63),(64,'2026-06-08 11:23:17.425078','2026-06-08 11:23:17.425078',50,64),(65,'2026-06-08 11:23:17.425654','2026-06-08 11:23:17.425654',50,65),(66,'2026-06-08 11:23:17.425654','2026-06-08 11:23:17.425654',50,66),(67,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161',50,67),(68,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161',50,68),(69,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161',50,69),(70,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161',50,70),(71,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196',50,71),(72,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196',50,72),(73,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196',50,73),(74,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196',50,74),(75,'2026-06-08 11:23:17.437742','2026-06-08 11:23:17.437742',50,75),(76,'2026-06-08 11:23:17.437742','2026-06-08 11:23:17.437742',50,76),(77,'2026-06-08 11:23:17.437742','2026-06-08 11:23:17.437742',50,77),(78,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',50,78),(79,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830',50,79);
/*!40000 ALTER TABLE `merchant_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merchant_inventory_record`
--

DROP TABLE IF EXISTS `merchant_inventory_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchant_inventory_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `before_stock` int unsigned NOT NULL,
  `after_stock` int unsigned NOT NULL,
  `reason` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `merchant_inventory_r_product_id_1066ecd3_fk_merchant_` (`product_id`),
  CONSTRAINT `merchant_inventory_r_product_id_1066ecd3_fk_merchant_` FOREIGN KEY (`product_id`) REFERENCES `merchant_product` (`id`),
  CONSTRAINT `merchant_inventory_record_chk_1` CHECK ((`before_stock` >= 0)),
  CONSTRAINT `merchant_inventory_record_chk_2` CHECK ((`after_stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant_inventory_record`
--

LOCK TABLES `merchant_inventory_record` WRITE;
/*!40000 ALTER TABLE `merchant_inventory_record` DISABLE KEYS */;
INSERT INTO `merchant_inventory_record` VALUES (1,'2026-06-08 11:23:17.350511','2026-06-08 11:23:17.350511','increase',0,50,'P3_REAL 初始测试库存',1),(2,'2026-06-08 11:23:17.352511','2026-06-08 11:23:17.352511','increase',0,50,'P3_REAL 初始测试库存',2),(3,'2026-06-08 11:23:17.353517','2026-06-08 11:23:17.353517','increase',0,50,'P3_REAL 初始测试库存',3),(4,'2026-06-08 11:23:17.354518','2026-06-08 11:23:17.354518','increase',0,50,'P3_REAL 初始测试库存',4),(5,'2026-06-08 11:23:17.356515','2026-06-08 11:23:17.356515','increase',0,50,'P3_REAL 初始测试库存',5),(6,'2026-06-08 11:23:17.356515','2026-06-08 11:23:17.356515','increase',0,50,'P3_REAL 初始测试库存',6),(7,'2026-06-08 11:23:17.358045','2026-06-08 11:23:17.358045','increase',0,50,'P3_REAL 初始测试库存',7),(8,'2026-06-08 11:23:17.359067','2026-06-08 11:23:17.359067','increase',0,50,'P3_REAL 初始测试库存',8),(9,'2026-06-08 11:23:17.361068','2026-06-08 11:23:17.361068','increase',0,50,'P3_REAL 初始测试库存',9),(10,'2026-06-08 11:23:17.362092','2026-06-08 11:23:17.362092','increase',0,50,'P3_REAL 初始测试库存',10),(11,'2026-06-08 11:23:17.362092','2026-06-08 11:23:17.362092','increase',0,50,'P3_REAL 初始测试库存',11),(12,'2026-06-08 11:23:17.362092','2026-06-08 11:23:17.362092','increase',0,50,'P3_REAL 初始测试库存',12),(13,'2026-06-08 11:23:17.365073','2026-06-08 11:23:17.365073','increase',0,50,'P3_REAL 初始测试库存',13),(14,'2026-06-08 11:23:17.365073','2026-06-08 11:23:17.365073','increase',0,50,'P3_REAL 初始测试库存',14),(15,'2026-06-08 11:23:17.368074','2026-06-08 11:23:17.368074','increase',0,50,'P3_REAL 初始测试库存',15),(16,'2026-06-08 11:23:17.368074','2026-06-08 11:23:17.368074','increase',0,50,'P3_REAL 初始测试库存',16),(17,'2026-06-08 11:23:17.368074','2026-06-08 11:23:17.368074','increase',0,50,'P3_REAL 初始测试库存',17),(18,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','increase',0,50,'P3_REAL 初始测试库存',18),(19,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','increase',0,50,'P3_REAL 初始测试库存',19),(20,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','increase',0,50,'P3_REAL 初始测试库存',20),(21,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','increase',0,50,'P3_REAL 初始测试库存',21),(22,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','increase',0,50,'P3_REAL 初始测试库存',22),(23,'2026-06-08 11:23:17.377110','2026-06-08 11:23:17.377110','increase',0,50,'P3_REAL 初始测试库存',23),(24,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199','increase',0,50,'P3_REAL 初始测试库存',24),(25,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199','increase',0,50,'P3_REAL 初始测试库存',25),(26,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199','increase',0,50,'P3_REAL 初始测试库存',26),(27,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199','increase',0,50,'P3_REAL 初始测试库存',27),(28,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','increase',0,50,'P3_REAL 初始测试库存',28),(29,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','increase',0,50,'P3_REAL 初始测试库存',29),(30,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','increase',0,50,'P3_REAL 初始测试库存',30),(31,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','increase',0,50,'P3_REAL 初始测试库存',31),(32,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','increase',0,50,'P3_REAL 初始测试库存',32),(33,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258','increase',0,50,'P3_REAL 初始测试库存',33),(34,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258','increase',0,50,'P3_REAL 初始测试库存',34),(35,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258','increase',0,50,'P3_REAL 初始测试库存',35),(36,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258','increase',0,50,'P3_REAL 初始测试库存',36),(37,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815','increase',0,50,'P3_REAL 初始测试库存',37),(38,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815','increase',0,50,'P3_REAL 初始测试库存',38),(39,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815','increase',0,50,'P3_REAL 初始测试库存',39),(40,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815','increase',0,50,'P3_REAL 初始测试库存',40),(41,'2026-06-08 11:23:17.396831','2026-06-08 11:23:17.396831','increase',0,50,'P3_REAL 初始测试库存',41),(42,'2026-06-08 11:23:17.397868','2026-06-08 11:23:17.397868','increase',0,50,'P3_REAL 初始测试库存',42),(43,'2026-06-08 11:23:17.398934','2026-06-08 11:23:17.398934','increase',0,50,'P3_REAL 初始测试库存',43),(44,'2026-06-08 11:23:17.400338','2026-06-08 11:23:17.400338','increase',0,50,'P3_REAL 初始测试库存',44),(45,'2026-06-08 11:23:17.401639','2026-06-08 11:23:17.401639','increase',0,50,'P3_REAL 初始测试库存',45),(46,'2026-06-08 11:23:17.402637','2026-06-08 11:23:17.402637','increase',0,50,'P3_REAL 初始测试库存',46),(47,'2026-06-08 11:23:17.403637','2026-06-08 11:23:17.403637','increase',0,50,'P3_REAL 初始测试库存',47),(48,'2026-06-08 11:23:17.404652','2026-06-08 11:23:17.404652','increase',0,50,'P3_REAL 初始测试库存',48),(49,'2026-06-08 11:23:17.405755','2026-06-08 11:23:17.405755','increase',0,50,'P3_REAL 初始测试库存',49),(50,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810','increase',0,50,'P3_REAL 初始测试库存',50),(51,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810','increase',0,50,'P3_REAL 初始测试库存',51),(52,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810','increase',0,50,'P3_REAL 初始测试库存',52),(53,'2026-06-08 11:23:17.413275','2026-06-08 11:23:17.413275','increase',0,50,'P3_REAL 初始测试库存',53),(54,'2026-06-08 11:23:17.414509','2026-06-08 11:23:17.414509','increase',0,50,'P3_REAL 初始测试库存',54),(55,'2026-06-08 11:23:17.415507','2026-06-08 11:23:17.415507','increase',0,50,'P3_REAL 初始测试库存',55),(56,'2026-06-08 11:23:17.416506','2026-06-08 11:23:17.416506','increase',0,50,'P3_REAL 初始测试库存',56),(57,'2026-06-08 11:23:17.416506','2026-06-08 11:23:17.416506','increase',0,50,'P3_REAL 初始测试库存',57),(58,'2026-06-08 11:23:17.419053','2026-06-08 11:23:17.419053','increase',0,50,'P3_REAL 初始测试库存',58),(59,'2026-06-08 11:23:17.420056','2026-06-08 11:23:17.420056','increase',0,50,'P3_REAL 初始测试库存',59),(60,'2026-06-08 11:23:17.421053','2026-06-08 11:23:17.421053','increase',0,50,'P3_REAL 初始测试库存',60),(61,'2026-06-08 11:23:17.422051','2026-06-08 11:23:17.422051','increase',0,50,'P3_REAL 初始测试库存',61),(62,'2026-06-08 11:23:17.423070','2026-06-08 11:23:17.423070','increase',0,50,'P3_REAL 初始测试库存',62),(63,'2026-06-08 11:23:17.424056','2026-06-08 11:23:17.424056','increase',0,50,'P3_REAL 初始测试库存',63),(64,'2026-06-08 11:23:17.425654','2026-06-08 11:23:17.425654','increase',0,50,'P3_REAL 初始测试库存',64),(65,'2026-06-08 11:23:17.425654','2026-06-08 11:23:17.425654','increase',0,50,'P3_REAL 初始测试库存',65),(66,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','increase',0,50,'P3_REAL 初始测试库存',66),(67,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','increase',0,50,'P3_REAL 初始测试库存',67),(68,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','increase',0,50,'P3_REAL 初始测试库存',68),(69,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','increase',0,50,'P3_REAL 初始测试库存',69),(70,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','increase',0,50,'P3_REAL 初始测试库存',70),(71,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196','increase',0,50,'P3_REAL 初始测试库存',71),(72,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196','increase',0,50,'P3_REAL 初始测试库存',72),(73,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196','increase',0,50,'P3_REAL 初始测试库存',73),(74,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196','increase',0,50,'P3_REAL 初始测试库存',74),(75,'2026-06-08 11:23:17.437742','2026-06-08 11:23:17.437742','increase',0,50,'P3_REAL 初始测试库存',75),(76,'2026-06-08 11:23:17.437742','2026-06-08 11:23:17.437742','increase',0,50,'P3_REAL 初始测试库存',76),(77,'2026-06-08 11:23:17.437742','2026-06-08 11:23:17.437742','increase',0,50,'P3_REAL 初始测试库存',77),(78,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830','increase',0,50,'P3_REAL 初始测试库存',78),(79,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830','increase',0,50,'P3_REAL 初始测试库存',79);
/*!40000 ALTER TABLE `merchant_inventory_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merchant_product`
--

DROP TABLE IF EXISTS `merchant_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchant_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rarity` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `estimated_points` int unsigned NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `review_note` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `merchant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `merchant_product_merchant_id_736f146f_fk_merchant_id` (`merchant_id`),
  CONSTRAINT `merchant_product_merchant_id_736f146f_fk_merchant_id` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`id`),
  CONSTRAINT `merchant_product_chk_1` CHECK ((`estimated_points` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant_product`
--

LOCK TABLES `merchant_product` WRITE;
/*!40000 ALTER TABLE `merchant_product` DISABLE KEYS */;
INSERT INTO `merchant_product` VALUES (1,'2026-06-08 11:23:17.349514','2026-06-08 11:23:17.349514','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','海报','R','EVA 海报周边，角色/主题：EVA 机体设定海报。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(2,'2026-06-08 11:23:17.351529','2026-06-08 11:23:17.351529','Saber誓约胜利之剑手办','/media/product/Saber誓约胜利之剑手办.png','手办','SSR','Fate 手办周边，角色/主题：Saber誓约胜利之剑手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(3,'2026-06-08 11:23:17.352511','2026-06-08 11:23:17.352511','《黑白的阿维斯塔》小说第一卷 凶战士篇','/media/product/《黑白的阿维斯塔》小说第一卷 凶战士篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第一卷 凶战士篇。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(4,'2026-06-08 11:23:17.354518','2026-06-08 11:23:17.354518','《黑白的阿维斯塔》小说第三卷 不变之物篇','/media/product/《黑白的阿维斯塔》小说第三卷 不变之物篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第三卷 不变之物篇。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(5,'2026-06-08 11:23:17.355550','2026-06-08 11:23:17.355550','《黑白的阿维斯塔》小说第二卷 惭愧之空篇','/media/product/《黑白的阿维斯塔》小说第二卷 惭愧之空篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第二卷 惭愧之空篇。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(6,'2026-06-08 11:23:17.356515','2026-06-08 11:23:17.356515','《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇','/media/product/《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(7,'2026-06-08 11:23:17.356515','2026-06-08 11:23:17.356515','丰缘三神','/media/product/丰缘三神.png','周边','SR','宝可梦 周边周边，角色/主题：丰缘三神。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(8,'2026-06-08 11:23:17.359067','2026-06-08 11:23:17.359067','乔巴冬岛毛绒玩偶','/media/product/乔巴冬岛毛绒玩偶.png','毛绒','R','海贼王 毛绒周边，角色/主题：乔巴冬岛毛绒玩偶。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(9,'2026-06-08 11:23:17.360068','2026-06-08 11:23:17.360068','乔鲁诺黄金体验徽章','/media/product/乔鲁诺黄金体验徽章.png','徽章','N','JOJO 徽章周边，角色/主题：乔鲁诺黄金体验徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(10,'2026-06-08 11:23:17.361068','2026-06-08 11:23:17.361068','五条悟无量空处手办','/media/product/五条悟无量空处手办.png','手办','SSR','咒术回战 手办周边，角色/主题：五条悟无量空处手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(11,'2026-06-08 11:23:17.362092','2026-06-08 11:23:17.362092','亚丝娜亚克力挂件','/media/product/亚丝娜亚克力挂件.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：亚丝娜亚克力挂件。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(12,'2026-06-08 11:23:17.362092','2026-06-08 11:23:17.362092','伏黑惠海报','/media/product/伏黑惠海报.png','海报','R','咒术回战 海报周边，角色/主题：伏黑惠海报。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(13,'2026-06-08 11:23:17.362092','2026-06-08 11:23:17.362092','佐助须佐能乎徽章','/media/product/佐助须佐能乎徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：佐助须佐能乎徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(14,'2026-06-08 11:23:17.365073','2026-06-08 11:23:17.365073','冈部伦太郎凤凰院徽章','/media/product/冈部伦太郎凤凰院徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：冈部伦太郎凤凰院徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(15,'2026-06-08 11:23:17.365073','2026-06-08 11:23:17.365073','凯尔希女仆亚克力立牌','/media/product/凯尔希女仆亚克力立牌.png','亚克力','SR','明日方舟 亚克力周边，角色/主题：凯尔希女仆亚克力立牌。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(16,'2026-06-08 11:23:17.368074','2026-06-08 11:23:17.368074','初号机金属徽章','/media/product/初号机金属徽章.png','徽章','SR','EVA 徽章周边，角色/主题：初号机金属徽章。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(17,'2026-06-08 11:23:17.368074','2026-06-08 11:23:17.368074','初音未来雪未来手办','/media/product/初音未来雪未来手办.png','手办','SSR','综合动漫 手办周边，角色/主题：初音未来雪未来手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(18,'2026-06-08 11:23:17.368074','2026-06-08 11:23:17.368074','劳埃德任务卡片','/media/product/劳埃德任务卡片.png','卡片','N','综合动漫 卡片周边，角色/主题：劳埃德任务卡片。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(19,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','卡卡西写轮眼海报','/media/product/卡卡西写轮眼海报.png','海报','R','综合动漫 海报周边，角色/主题：卡卡西写轮眼海报。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(20,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','史尔特尔主题立牌','/media/product/史尔特尔主题立牌.png','亚克力','SR','明日方舟 亚克力周边，角色/主题：史尔特尔主题立牌。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(21,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','喜多川海梦水族馆立牌','/media/product/喜多川海梦水族馆立牌.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：喜多川海梦水族馆立牌。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(22,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','嘴平伊之助毛绒挂件','/media/product/嘴平伊之助毛绒挂件.png','毛绒','R','鬼灭之刃 毛绒周边，角色/主题：嘴平伊之助毛绒挂件。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(23,'2026-06-08 11:23:17.371079','2026-06-08 11:23:17.371079','夜刀神十香灵装徽章','/media/product/夜刀神十香灵装徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：夜刀神十香灵装徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(24,'2026-06-08 11:23:17.377110','2026-06-08 11:23:17.377110','奶龙真实身份证据','/media/product/奶龙真实身份证据.png','周边','N','综合动漫 周边周边，角色/主题：奶龙真实身份证据。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(25,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199','娜美航海图卡套','/media/product/娜美航海图卡套.png','周边','N','海贼王 周边周边，角色/主题：娜美航海图卡套。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(26,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199','宇智波鼬亚克力','/media/product/宇智波鼬亚克力.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：宇智波鼬亚克力。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(27,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199','帕瓦恶魔角徽章','/media/product/帕瓦恶魔角徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：帕瓦恶魔角徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(28,'2026-06-08 11:23:17.378199','2026-06-08 11:23:17.378199','我妻善逸雷之呼吸徽章','/media/product/我妻善逸雷之呼吸徽章.png','徽章','N','鬼灭之刃 徽章周边，角色/主题：我妻善逸雷之呼吸徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(29,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','拉姆女仆徽章','/media/product/拉姆女仆徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：拉姆女仆徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(30,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','斗牌传说赤木海报','/media/product/斗牌传说赤木海报.png','海报','R','综合动漫 海报周边，角色/主题：斗牌传说赤木海报。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(31,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','早川秋海报','/media/product/早川秋海报.png','海报','R','综合动漫 海报周边，角色/主题：早川秋海报。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(32,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','时崎狂三哥特手办','/media/product/时崎狂三哥特手办.png','手办','SSR','综合动漫 手办周边，角色/主题：时崎狂三哥特手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(33,'2026-06-08 11:23:17.383236','2026-06-08 11:23:17.383236','明日香红色驾驶服手办','/media/product/明日香红色驾驶服手办.png','手办','SSR','EVA 手办周边，角色/主题：明日香红色驾驶服手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(34,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258','明日香限定卡片','/media/product/明日香限定卡片.png','卡片','SR','EVA 卡片周边，角色/主题：明日香限定卡片。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(35,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258','星野爱徽章','/media/product/星野爱徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：星野爱徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(36,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258','春日限定徽章','/media/product/春日限定徽章.png','徽章','SR','综合动漫 徽章周边，角色/主题：春日限定徽章。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(37,'2026-06-08 11:23:17.388258','2026-06-08 11:23:17.388258','有马加奈角色立牌','/media/product/有马加奈角色立牌.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：有马加奈角色立牌。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(38,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815','枫原万叶流沙亚克力','/media/product/枫原万叶流沙亚克力.png','亚克力','SR','原神 亚克力周边，角色/主题：枫原万叶流沙亚克力。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(39,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815','森蚺手办','/media/product/森蚺手办.png','手办','SSR','明日方舟 手办周边，角色/主题：森蚺手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(40,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815','沙奈朵手办','/media/product/沙奈朵手办.png','手办','SSR','宝可梦 手办周边，角色/主题：沙奈朵手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(41,'2026-06-08 11:23:17.392815','2026-06-08 11:23:17.392815','波奇塔毛绒挂件','/media/product/波奇塔毛绒挂件.png','毛绒','R','综合动漫 毛绒周边，角色/主题：波奇塔毛绒挂件。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(42,'2026-06-08 11:23:17.396831','2026-06-08 11:23:17.396831','浊心斯卡蒂深海主题徽章','/media/product/浊心斯卡蒂深海主题徽章.png','徽章','N','明日方舟 徽章周边，角色/主题：浊心斯卡蒂深海主题徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(43,'2026-06-08 11:23:17.397868','2026-06-08 11:23:17.397868','火陈通行证挂件','/media/product/火陈通行证挂件.png','挂件','N','综合动漫 挂件周边，角色/主题：火陈通行证挂件。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(44,'2026-06-08 11:23:17.399380','2026-06-08 11:23:17.399380','灶门炭治郎水之呼吸手办','/media/product/灶门炭治郎水之呼吸手办.png','手办','SSR','鬼灭之刃 手办周边，角色/主题：灶门炭治郎水之呼吸手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(45,'2026-06-08 11:23:17.400338','2026-06-08 11:23:17.400338','炭治郎日轮刀模型','/media/product/炭治郎日轮刀模型.png','手办','SSR','鬼灭之刃 手办周边，角色/主题：炭治郎日轮刀模型。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(46,'2026-06-08 11:23:17.401639','2026-06-08 11:23:17.401639','爱蜜莉雅雪花手办','/media/product/爱蜜莉雅雪花手办.png','手办','SSR','综合动漫 手办周边，角色/主题：爱蜜莉雅雪花手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(47,'2026-06-08 11:23:17.403637','2026-06-08 11:23:17.403637','牧濑红莉栖实验室手办','/media/product/牧濑红莉栖实验室手办.png','手办','SSR','综合动漫 手办周边，角色/主题：牧濑红莉栖实验室手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(48,'2026-06-08 11:23:17.404652','2026-06-08 11:23:17.404652','由比滨结衣亚克力挂件','/media/product/由比滨结衣亚克力挂件.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：由比滨结衣亚克力挂件。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(49,'2026-06-08 11:23:17.405755','2026-06-08 11:23:17.405755','电次电锯形态手办','/media/product/电次电锯形态手办.png','手办','SSR','综合动漫 手办周边，角色/主题：电次电锯形态手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(50,'2026-06-08 11:23:17.406770','2026-06-08 11:23:17.406770','皮卡丘毛绒玩偶','/media/product/皮卡丘毛绒玩偶.png','毛绒','R','宝可梦 毛绒周边，角色/主题：皮卡丘毛绒玩偶。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(51,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810','祢豆子竹筒玩偶','/media/product/祢豆子竹筒玩偶.png','毛绒','R','鬼灭之刃 毛绒周边，角色/主题：祢豆子竹筒玩偶。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(52,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810','空条承太郎白金之星手办','/media/product/空条承太郎白金之星手办.png','手办','SSR','JOJO 手办周边，角色/主题：空条承太郎白金之星手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(53,'2026-06-08 11:23:17.407810','2026-06-08 11:23:17.407810','索隆三刀流亚克力','/media/product/索隆三刀流亚克力.png','亚克力','SR','海贼王 亚克力周边，角色/主题：索隆三刀流亚克力。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(54,'2026-06-08 11:23:17.413275','2026-06-08 11:23:17.413275','约尔亚克力','/media/product/约尔亚克力.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：约尔亚克力。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(55,'2026-06-08 11:23:17.414509','2026-06-08 11:23:17.414509','纳西妲立牌','/media/product/纳西妲立牌.png','亚克力','SR','原神 亚克力周边，角色/主题：纳西妲立牌。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(56,'2026-06-08 11:23:17.415507','2026-06-08 11:23:17.415507','绫波丽白色驾驶服手办','/media/product/绫波丽白色驾驶服手办.png','手办','SSR','EVA 手办周边，角色/主题：绫波丽白色驾驶服手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(57,'2026-06-08 11:23:17.416506','2026-06-08 11:23:17.416506','能天使拉特兰亚克力立牌','/media/product/能天使拉特兰亚克力立牌.png','亚克力','SR','明日方舟 亚克力周边，角色/主题：能天使拉特兰亚克力立牌。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(58,'2026-06-08 11:23:17.418034','2026-06-08 11:23:17.418034','艾雅法拉手办','/media/product/艾雅法拉手办.png','手办','SSR','明日方舟 手办周边，角色/主题：艾雅法拉手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(59,'2026-06-08 11:23:17.419053','2026-06-08 11:23:17.419053','芙宁娜纪念卡册','/media/product/芙宁娜纪念卡册.png','卡册','R','原神 卡册周边，角色/主题：芙宁娜纪念卡册。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(60,'2026-06-08 11:23:17.420056','2026-06-08 11:23:17.420056','蕾姆拉姆双人色纸','/media/product/蕾姆拉姆双人色纸.png','色纸','SR','综合动漫 色纸周边，角色/主题：蕾姆拉姆双人色纸。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(61,'2026-06-08 11:23:17.421053','2026-06-08 11:23:17.421053','蕾姆泳装手办','/media/product/蕾姆泳装手办.png','手办','SSR','综合动漫 手办周边，角色/主题：蕾姆泳装手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(62,'2026-06-08 11:23:17.422051','2026-06-08 11:23:17.422051','虎杖悠仁战斗徽章','/media/product/虎杖悠仁战斗徽章.png','徽章','N','咒术回战 徽章周边，角色/主题：虎杖悠仁战斗徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(63,'2026-06-08 11:23:17.423070','2026-06-08 11:23:17.423070','蝴蝶忍色纸','/media/product/蝴蝶忍色纸.png','色纸','SR','鬼灭之刃 色纸周边，角色/主题：蝴蝶忍色纸。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(64,'2026-06-08 11:23:17.425078','2026-06-08 11:23:17.425078','超梦手办','/media/product/超梦手办.png','手办','SSR','宝可梦 手办周边，角色/主题：超梦手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(65,'2026-06-08 11:23:17.425654','2026-06-08 11:23:17.425654','路飞五档海报','/media/product/路飞五档海报.png','海报','R','海贼王 海报周边，角色/主题：路飞五档海报。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(66,'2026-06-08 11:23:17.425654','2026-06-08 11:23:17.425654','路飞尼卡手办','/media/product/路飞尼卡手办.png','手办','SSR','海贼王 手办周边，角色/主题：路飞尼卡手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(67,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','远坂凛宝石魔术徽章','/media/product/远坂凛宝石魔术徽章.png','徽章','N','Fate 徽章周边，角色/主题：远坂凛宝石魔术徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(68,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','钉崎野蔷薇亚克力挂件','/media/product/钉崎野蔷薇亚克力挂件.png','亚克力','SR','咒术回战 亚克力周边，角色/主题：钉崎野蔷薇亚克力挂件。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(69,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','钟离烫金色纸','/media/product/钟离烫金色纸.png','色纸','SSR','原神 色纸周边，角色/主题：钟离烫金色纸。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(70,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','银灰谢拉格收藏立牌','/media/product/银灰谢拉格收藏立牌.png','亚克力','SR','明日方舟 亚克力周边，角色/主题：银灰谢拉格收藏立牌。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(71,'2026-06-08 11:23:17.428161','2026-06-08 11:23:17.428161','间桐樱樱花亚克力','/media/product/间桐樱樱花亚克力.png','亚克力','SR','Fate 亚克力周边，角色/主题：间桐樱樱花亚克力。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(72,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196','阿尼亚校服毛绒玩偶','/media/product/阿尼亚校服毛绒玩偶.png','毛绒','R','综合动漫 毛绒周边，角色/主题：阿尼亚校服毛绒玩偶。用于P3盲盒抽取、我的资产和换物测试。',160,'approved','P3_REAL seed',1),(73,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196','阿尼亚表情包立牌','/media/product/阿尼亚表情包立牌.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：阿尼亚表情包立牌。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(74,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196','阿米娅罗德岛徽章','/media/product/阿米娅罗德岛徽章.png','徽章','N','明日方舟 徽章周边，角色/主题：阿米娅罗德岛徽章。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1),(75,'2026-06-08 11:23:17.433196','2026-06-08 11:23:17.433196','雪之下雪乃校园色纸','/media/product/雪之下雪乃校园色纸.png','色纸','SR','综合动漫 色纸周边，角色/主题：雪之下雪乃校园色纸。用于P3盲盒抽取、我的资产和换物测试。',300,'approved','P3_REAL seed',1),(76,'2026-06-08 11:23:17.437742','2026-06-08 11:23:17.437742','雷电影主题徽章套装','/media/product/雷电影主题徽章套装.png','徽章','SSR','原神 徽章周边，角色/主题：雷电影主题徽章套装。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(77,'2026-06-08 11:23:17.437742','2026-06-08 11:23:17.437742','骑拉帝纳','/media/product/骑拉帝纳.png','周边','SSR','宝可梦 周边周边，角色/主题：骑拉帝纳。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(78,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830','鸣人九尾查克拉手办','/media/product/鸣人九尾查克拉手办.png','手办','SSR','综合动漫 手办周边，角色/主题：鸣人九尾查克拉手办。用于P3盲盒抽取、我的资产和换物测试。',520,'approved','P3_REAL seed',1),(79,'2026-06-08 11:23:17.440830','2026-06-08 11:23:17.440830','黑川茜收藏卡','/media/product/黑川茜收藏卡.png','周边','N','综合动漫 周边周边，角色/主题：黑川茜收藏卡。用于P3盲盒抽取、我的资产和换物测试。',80,'approved','P3_REAL seed',1);
/*!40000 ALTER TABLE `merchant_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merchant_shipment`
--

DROP TABLE IF EXISTS `merchant_shipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchant_shipment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `task_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_phone` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `logistics_company` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tracking_no` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shipped_at` datetime(6) DEFAULT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `merchant_shipment_product_id_f8259f62_fk_merchant_product_id` (`product_id`),
  CONSTRAINT `merchant_shipment_product_id_f8259f62_fk_merchant_product_id` FOREIGN KEY (`product_id`) REFERENCES `merchant_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant_shipment`
--

LOCK TABLES `merchant_shipment` WRITE;
/*!40000 ALTER TABLE `merchant_shipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `merchant_shipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_log`
--

DROP TABLE IF EXISTS `operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `operator` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `target` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `detail` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_log`
--

LOCK TABLES `operation_log` WRITE;
/*!40000 ALTER TABLE `operation_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `operation_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `asset_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `asset_image` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_phone` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `logistics_company` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tracking_no` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shipped_at` datetime(6) DEFAULT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `asset_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `order_asset_id_ec0a3fbb_fk_user_asset_id` (`asset_id`),
  KEY `order_user_id_e323497c_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `order_asset_id_ec0a3fbb_fk_user_asset_id` FOREIGN KEY (`asset_id`) REFERENCES `user_asset` (`id`),
  CONSTRAINT `order_user_id_e323497c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `points_account`
--

DROP TABLE IF EXISTS `points_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `points_account` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `balance` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `points_account_user_id_0c89d2bb_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_account`
--

LOCK TABLES `points_account` WRITE;
/*!40000 ALTER TABLE `points_account` DISABLE KEYS */;
INSERT INTO `points_account` VALUES (1,'2026-06-08 11:23:17.340790','2026-06-08 11:23:17.340790',10620,4),(2,'2026-06-08 11:23:17.343305','2026-06-08 11:23:17.343305',10000,5);
/*!40000 ALTER TABLE `points_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `points_record`
--

DROP TABLE IF EXISTS `points_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `points_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` int NOT NULL,
  `balance` int NOT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `related_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `points_record_user_id_686f577b_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `points_record_user_id_686f577b_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_record`
--

LOCK TABLES `points_record` WRITE;
/*!40000 ALTER TABLE `points_record` DISABLE KEYS */;
INSERT INTO `points_record` VALUES (1,'2026-06-08 11:23:17.341799','2026-06-08 11:23:17.341799','system_adjust',10000,10000,'P3_REAL 测试积分初始化','P3_REAL',4),(2,'2026-06-08 11:23:17.343992','2026-06-08 11:23:17.343992','system_adjust',10000,10000,'P3_REAL 测试积分初始化','P3_REAL',5),(3,'2026-06-08 11:27:24.525030','2026-06-08 11:27:24.525030','blindbox_consume',-1000,9000,'抽取P3真实EVA主题盲盒 x10','B20260608112724EC017E',4),(4,'2026-06-08 11:27:26.067876','2026-06-08 11:27:26.067876','recycle_return',1620,10620,'批量回收10件资产','RBBE1C1EE7EB6D',4);
/*!40000 ALTER TABLE `points_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rule_config`
--

DROP TABLE IF EXISTS `rule_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rule_config` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `recycle_rate` int unsigned NOT NULL,
  `new_user_points` int unsigned NOT NULL,
  `max_draw_per_day` int unsigned NOT NULL,
  `min_points_to_draw` int unsigned NOT NULL,
  `order_auto_confirm_days` int unsigned NOT NULL,
  `exchange_lock_hours` int unsigned NOT NULL,
  `updated_by` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `rule_config_chk_1` CHECK ((`recycle_rate` >= 0)),
  CONSTRAINT `rule_config_chk_2` CHECK ((`new_user_points` >= 0)),
  CONSTRAINT `rule_config_chk_3` CHECK ((`max_draw_per_day` >= 0)),
  CONSTRAINT `rule_config_chk_4` CHECK ((`min_points_to_draw` >= 0)),
  CONSTRAINT `rule_config_chk_5` CHECK ((`order_auto_confirm_days` >= 0)),
  CONSTRAINT `rule_config_chk_6` CHECK ((`exchange_lock_hours` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rule_config`
--

LOCK TABLES `rule_config` WRITE;
/*!40000 ALTER TABLE `rule_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `rule_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_ledger`
--

DROP TABLE IF EXISTS `transaction_ledger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_ledger` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_ledger`
--

LOCK TABLES `transaction_ledger` WRITE;
/*!40000 ALTER TABLE `transaction_ledger` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction_ledger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_record`
--

DROP TABLE IF EXISTS `transaction_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `related_asset_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status_change` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transaction_record_user_id_d411c717_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `transaction_record_user_id_d411c717_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_record`
--

LOCK TABLES `transaction_record` WRITE;
/*!40000 ALTER TABLE `transaction_record` DISABLE KEYS */;
INSERT INTO `transaction_record` VALUES (1,'2026-06-08 11:27:26.055806','2026-06-08 11:27:26.055806','recycle','回收明日香红色驾驶服手办','明日香红色驾驶服手办','available -> recycled',4),(2,'2026-06-08 11:27:26.056807','2026-06-08 11:27:26.056807','recycle','回收明日香限定卡片','明日香限定卡片','available -> recycled',4),(3,'2026-06-08 11:27:26.058531','2026-06-08 11:27:26.058531','recycle','回收明日香限定卡片','明日香限定卡片','available -> recycled',4),(4,'2026-06-08 11:27:26.059539','2026-06-08 11:27:26.059539','recycle','回收明日香限定卡片','明日香限定卡片','available -> recycled',4),(5,'2026-06-08 11:27:26.061543','2026-06-08 11:27:26.061543','recycle','回收初号机金属徽章','初号机金属徽章','available -> recycled',4),(6,'2026-06-08 11:27:26.062538','2026-06-08 11:27:26.062538','recycle','回收EVA 机体设定海报','EVA 机体设定海报','available -> recycled',4),(7,'2026-06-08 11:27:26.063539','2026-06-08 11:27:26.063539','recycle','回收EVA 机体设定海报','EVA 机体设定海报','available -> recycled',4),(8,'2026-06-08 11:27:26.064538','2026-06-08 11:27:26.064538','recycle','回收绫波丽白色驾驶服手办','绫波丽白色驾驶服手办','available -> recycled',4),(9,'2026-06-08 11:27:26.065540','2026-06-08 11:27:26.065540','recycle','回收EVA 机体设定海报','EVA 机体设定海报','available -> recycled',4),(10,'2026-06-08 11:27:26.066538','2026-06-08 11:27:26.066538','recycle','回收绫波丽白色驾驶服手办','绫波丽白色驾驶服手办','available -> recycled',4);
/*!40000 ALTER TABLE `transaction_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_address`
--

DROP TABLE IF EXISTS `user_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_address` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `receiver_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_phone` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `street` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `detail` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  `city_id` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `district_id` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `province_id` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_address_user_id_64deb2c7_fk_accounts_user_id` (`user_id`),
  KEY `user_address_city_id_654faf8b_fk_division_code` (`city_id`),
  KEY `user_address_district_id_c5436367_fk_division_code` (`district_id`),
  KEY `user_address_province_id_05547a59_fk_division_code` (`province_id`),
  CONSTRAINT `user_address_city_id_654faf8b_fk_division_code` FOREIGN KEY (`city_id`) REFERENCES `division` (`code`),
  CONSTRAINT `user_address_district_id_c5436367_fk_division_code` FOREIGN KEY (`district_id`) REFERENCES `division` (`code`),
  CONSTRAINT `user_address_province_id_05547a59_fk_division_code` FOREIGN KEY (`province_id`) REFERENCES `division` (`code`),
  CONSTRAINT `user_address_user_id_64deb2c7_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_address`
--

LOCK TABLES `user_address` WRITE;
/*!40000 ALTER TABLE `user_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_asset`
--

DROP TABLE IF EXISTS `user_asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_asset` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `product_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_image` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rarity` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `obtained_at` datetime(6) NOT NULL,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estimated_points` int unsigned NOT NULL,
  `recyclable_points` int unsigned NOT NULL,
  `draw_record_id` bigint DEFAULT NULL,
  `product_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_asset_draw_record_id_9e7734de_fk_blindbox_draw_record_id` (`draw_record_id`),
  KEY `user_asset_product_id_00ee943d_fk_merchant_product_id` (`product_id`),
  KEY `user_asset_user_id_01801462_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `user_asset_draw_record_id_9e7734de_fk_blindbox_draw_record_id` FOREIGN KEY (`draw_record_id`) REFERENCES `blindbox_draw_record` (`id`),
  CONSTRAINT `user_asset_product_id_00ee943d_fk_merchant_product_id` FOREIGN KEY (`product_id`) REFERENCES `merchant_product` (`id`),
  CONSTRAINT `user_asset_user_id_01801462_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `user_asset_chk_1` CHECK ((`estimated_points` >= 0)),
  CONSTRAINT `user_asset_chk_2` CHECK ((`recyclable_points` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_asset`
--

LOCK TABLES `user_asset` WRITE;
/*!40000 ALTER TABLE `user_asset` DISABLE KEYS */;
INSERT INTO `user_asset` VALUES (1,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','海报','R','EVA 海报周边，角色/主题：EVA 机体设定海报。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 11:23:17.468009','available',160,80,NULL,1,4),(2,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009','Saber誓约胜利之剑手办','/media/product/Saber誓约胜利之剑手办.png','手办','SSR','Fate 手办周边，角色/主题：Saber誓约胜利之剑手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 11:20:17.468009','available',520,260,NULL,2,4),(3,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009','《黑白的阿维斯塔》小说第一卷 凶战士篇','/media/product/《黑白的阿维斯塔》小说第一卷 凶战士篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第一卷 凶战士篇。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 11:17:17.468009','available',160,80,NULL,3,4),(4,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009','《黑白的阿维斯塔》小说第三卷 不变之物篇','/media/product/《黑白的阿维斯塔》小说第三卷 不变之物篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第三卷 不变之物篇。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 11:14:17.468009','available',160,80,NULL,4,4),(5,'2026-06-08 11:23:17.468009','2026-06-08 11:23:17.468009','《黑白的阿维斯塔》小说第二卷 惭愧之空篇','/media/product/《黑白的阿维斯塔》小说第二卷 惭愧之空篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第二卷 惭愧之空篇。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 11:11:17.468009','available',160,80,NULL,5,4),(6,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇','/media/product/《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 11:08:17.468009','available',160,80,NULL,6,4),(7,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','丰缘三神','/media/product/丰缘三神.png','周边','SR','宝可梦 周边周边，角色/主题：丰缘三神。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 11:05:17.468009','available',300,150,NULL,7,4),(8,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','乔巴冬岛毛绒玩偶','/media/product/乔巴冬岛毛绒玩偶.png','毛绒','R','海贼王 毛绒周边，角色/主题：乔巴冬岛毛绒玩偶。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 11:02:17.468009','recycled',160,80,NULL,8,4),(9,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','乔鲁诺黄金体验徽章','/media/product/乔鲁诺黄金体验徽章.png','徽章','N','JOJO 徽章周边，角色/主题：乔鲁诺黄金体验徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:59:17.468009','available',80,40,NULL,9,4),(10,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','五条悟无量空处手办','/media/product/五条悟无量空处手办.png','手办','SSR','咒术回战 手办周边，角色/主题：五条悟无量空处手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:56:17.468009','available',520,260,NULL,10,4),(11,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','亚丝娜亚克力挂件','/media/product/亚丝娜亚克力挂件.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：亚丝娜亚克力挂件。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:53:17.468009','available',300,150,NULL,11,4),(12,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','伏黑惠海报','/media/product/伏黑惠海报.png','海报','R','咒术回战 海报周边，角色/主题：伏黑惠海报。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:50:17.468009','available',160,80,NULL,12,4),(13,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','佐助须佐能乎徽章','/media/product/佐助须佐能乎徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：佐助须佐能乎徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:47:17.468009','available',80,40,NULL,13,4),(14,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','冈部伦太郎凤凰院徽章','/media/product/冈部伦太郎凤凰院徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：冈部伦太郎凤凰院徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:44:17.468009','available',80,40,NULL,14,4),(15,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','凯尔希女仆亚克力立牌','/media/product/凯尔希女仆亚克力立牌.png','亚克力','SR','明日方舟 亚克力周边，角色/主题：凯尔希女仆亚克力立牌。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:41:17.468009','available',300,150,NULL,15,4),(16,'2026-06-08 11:23:17.473221','2026-06-08 11:23:17.473221','初号机金属徽章','/media/product/初号机金属徽章.png','徽章','SR','EVA 徽章周边，角色/主题：初号机金属徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:38:17.468009','recycled',300,150,NULL,16,4),(17,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','初音未来雪未来手办','/media/product/初音未来雪未来手办.png','手办','SSR','综合动漫 手办周边，角色/主题：初音未来雪未来手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:35:17.468009','available',520,260,NULL,17,4),(18,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','劳埃德任务卡片','/media/product/劳埃德任务卡片.png','卡片','N','综合动漫 卡片周边，角色/主题：劳埃德任务卡片。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:32:17.468009','available',80,40,NULL,18,4),(19,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','卡卡西写轮眼海报','/media/product/卡卡西写轮眼海报.png','海报','R','综合动漫 海报周边，角色/主题：卡卡西写轮眼海报。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:29:17.468009','available',160,80,NULL,19,4),(20,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','史尔特尔主题立牌','/media/product/史尔特尔主题立牌.png','亚克力','SR','明日方舟 亚克力周边，角色/主题：史尔特尔主题立牌。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:26:17.468009','available',300,150,NULL,20,4),(21,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','喜多川海梦水族馆立牌','/media/product/喜多川海梦水族馆立牌.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：喜多川海梦水族馆立牌。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:23:17.468009','available',300,150,NULL,21,4),(22,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','嘴平伊之助毛绒挂件','/media/product/嘴平伊之助毛绒挂件.png','毛绒','R','鬼灭之刃 毛绒周边，角色/主题：嘴平伊之助毛绒挂件。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:20:17.468009','available',160,80,NULL,22,4),(23,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','夜刀神十香灵装徽章','/media/product/夜刀神十香灵装徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：夜刀神十香灵装徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:17:17.468009','available',80,40,NULL,23,4),(24,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','奶龙真实身份证据','/media/product/奶龙真实身份证据.png','周边','N','综合动漫 周边周边，角色/主题：奶龙真实身份证据。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:14:17.468009','recycled',80,40,NULL,24,4),(25,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','娜美航海图卡套','/media/product/娜美航海图卡套.png','周边','N','海贼王 周边周边，角色/主题：娜美航海图卡套。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:11:17.468009','available',80,40,NULL,25,4),(26,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','宇智波鼬亚克力','/media/product/宇智波鼬亚克力.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：宇智波鼬亚克力。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:08:17.468009','available',300,150,NULL,26,4),(27,'2026-06-08 11:23:17.478264','2026-06-08 11:23:17.478264','帕瓦恶魔角徽章','/media/product/帕瓦恶魔角徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：帕瓦恶魔角徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:05:17.468009','available',80,40,NULL,27,4),(28,'2026-06-08 11:23:17.482820','2026-06-08 11:23:17.482820','我妻善逸雷之呼吸徽章','/media/product/我妻善逸雷之呼吸徽章.png','徽章','N','鬼灭之刃 徽章周边，角色/主题：我妻善逸雷之呼吸徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 10:02:17.468009','available',80,40,NULL,28,4),(29,'2026-06-08 11:23:17.482820','2026-06-08 11:23:17.482820','拉姆女仆徽章','/media/product/拉姆女仆徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：拉姆女仆徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 09:59:17.468009','available',80,40,NULL,29,4),(30,'2026-06-08 11:23:17.482820','2026-06-08 11:23:17.482820','斗牌传说赤木海报','/media/product/斗牌传说赤木海报.png','海报','R','综合动漫 海报周边，角色/主题：斗牌传说赤木海报。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 09:56:17.468009','available',160,80,NULL,30,4),(31,'2026-06-08 11:23:17.483829','2026-06-08 11:23:17.484194','早川秋海报','/media/product/早川秋海报.png','海报','R','综合动漫 海报周边，角色/主题：早川秋海报。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 09:53:17.468009','available',160,80,NULL,31,4),(32,'2026-06-08 11:23:17.484194','2026-06-08 11:23:17.484194','时崎狂三哥特手办','/media/product/时崎狂三哥特手办.png','手办','SSR','综合动漫 手办周边，角色/主题：时崎狂三哥特手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 09:50:17.468009','available',520,260,NULL,32,4),(33,'2026-06-08 11:23:17.484194','2026-06-08 11:23:17.484194','明日香红色驾驶服手办','/media/product/明日香红色驾驶服手办.png','手办','SSR','EVA 手办周边，角色/主题：明日香红色驾驶服手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 09:47:17.468009','available',520,260,NULL,33,4),(34,'2026-06-08 11:23:17.484194','2026-06-08 11:23:17.484194','明日香限定卡片','/media/product/明日香限定卡片.png','卡片','SR','EVA 卡片周边，角色/主题：明日香限定卡片。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 09:44:17.468009','available',300,150,NULL,34,4),(35,'2026-06-08 11:23:17.484194','2026-06-08 11:23:17.484194','星野爱徽章','/media/product/星野爱徽章.png','徽章','N','综合动漫 徽章周边，角色/主题：星野爱徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 09:41:17.468009','available',80,40,NULL,35,4),(36,'2026-06-08 11:23:17.486260','2026-06-08 11:23:17.486260','春日限定徽章','/media/product/春日限定徽章.png','徽章','SR','综合动漫 徽章周边，角色/主题：春日限定徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 我的资产测试','2026-06-08 09:38:17.468009','available',300,150,NULL,36,4),(37,'2026-06-08 11:23:17.486260','2026-06-08 11:23:17.486260','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','海报','R','EVA 海报周边，角色/主题：EVA 机体设定海报。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 同类保留测试','2026-06-08 11:23:17.468009','available',160,80,NULL,1,4),(38,'2026-06-08 11:23:17.486260','2026-06-08 11:23:17.486260','Saber誓约胜利之剑手办','/media/product/Saber誓约胜利之剑手办.png','手办','SSR','Fate 手办周边，角色/主题：Saber誓约胜利之剑手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 同类保留测试','2026-06-08 11:23:17.468009','available',520,260,NULL,2,4),(39,'2026-06-08 11:23:17.487770','2026-06-08 11:23:17.487770','《黑白的阿维斯塔》小说第一卷 凶战士篇','/media/product/《黑白的阿维斯塔》小说第一卷 凶战士篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第一卷 凶战士篇。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 同类保留测试','2026-06-08 11:23:17.468009','available',160,80,NULL,3,4),(40,'2026-06-08 11:23:17.487770','2026-06-08 11:23:17.487770','《黑白的阿维斯塔》小说第三卷 不变之物篇','/media/product/《黑白的阿维斯塔》小说第三卷 不变之物篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第三卷 不变之物篇。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 同类保留测试','2026-06-08 11:23:17.468009','available',160,80,NULL,4,4),(41,'2026-06-08 11:23:17.488825','2026-06-08 11:23:17.488825','《黑白的阿维斯塔》小说第二卷 惭愧之空篇','/media/product/《黑白的阿维斯塔》小说第二卷 惭愧之空篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第二卷 惭愧之空篇。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 同类保留测试','2026-06-08 11:23:17.468009','available',160,80,NULL,5,4),(42,'2026-06-08 11:23:17.488825','2026-06-08 11:23:17.488825','《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇','/media/product/《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇.jpg','小说','R','黑白的阿维斯塔 小说周边，角色/主题：《黑白的阿维斯塔》小说第四卷 堕天无惭乐土篇。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 同类保留测试','2026-06-08 11:23:17.468009','available',160,80,NULL,6,4),(43,'2026-06-08 11:23:17.488825','2026-06-08 11:23:17.488825','丰缘三神','/media/product/丰缘三神.png','周边','SR','宝可梦 周边周边，角色/主题：丰缘三神。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 同类保留测试','2026-06-08 11:23:17.468009','available',300,150,NULL,7,4),(44,'2026-06-08 11:23:17.489817','2026-06-08 11:23:17.489817','乔巴冬岛毛绒玩偶','/media/product/乔巴冬岛毛绒玩偶.png','毛绒','R','海贼王 毛绒周边，角色/主题：乔巴冬岛毛绒玩偶。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 同类保留测试','2026-06-08 11:23:17.468009','available',160,80,NULL,8,4),(45,'2026-06-08 11:23:17.489817','2026-06-08 11:23:17.498291','有马加奈角色立牌','/media/product/有马加奈角色立牌.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：有马加奈角色立牌。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:23:17.468009','exchange_published',300,150,NULL,37,5),(46,'2026-06-08 11:23:17.491814','2026-06-08 11:23:17.498291','枫原万叶流沙亚克力','/media/product/枫原万叶流沙亚克力.png','亚克力','SR','原神 亚克力周边，角色/主题：枫原万叶流沙亚克力。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:21:17.468009','exchange_published',300,150,NULL,38,5),(47,'2026-06-08 11:23:17.491814','2026-06-08 11:23:17.498291','森蚺手办','/media/product/森蚺手办.png','手办','SSR','明日方舟 手办周边，角色/主题：森蚺手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:19:17.468009','exchange_published',520,260,NULL,39,5),(48,'2026-06-08 11:23:17.492781','2026-06-08 11:23:17.498291','沙奈朵手办','/media/product/沙奈朵手办.png','手办','SSR','宝可梦 手办周边，角色/主题：沙奈朵手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:17:17.468009','exchange_published',520,260,NULL,40,5),(49,'2026-06-08 11:23:17.492781','2026-06-08 11:23:17.498291','波奇塔毛绒挂件','/media/product/波奇塔毛绒挂件.png','毛绒','R','综合动漫 毛绒周边，角色/主题：波奇塔毛绒挂件。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:15:17.468009','exchange_published',160,80,NULL,41,5),(50,'2026-06-08 11:23:17.493779','2026-06-08 11:23:17.504480','浊心斯卡蒂深海主题徽章','/media/product/浊心斯卡蒂深海主题徽章.png','徽章','N','明日方舟 徽章周边，角色/主题：浊心斯卡蒂深海主题徽章。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:13:17.468009','exchange_published',80,40,NULL,42,5),(51,'2026-06-08 11:23:17.493779','2026-06-08 11:23:17.504480','火陈通行证挂件','/media/product/火陈通行证挂件.png','挂件','N','综合动漫 挂件周边，角色/主题：火陈通行证挂件。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:11:17.468009','exchange_published',80,40,NULL,43,5),(52,'2026-06-08 11:23:17.494778','2026-06-08 11:23:17.504480','灶门炭治郎水之呼吸手办','/media/product/灶门炭治郎水之呼吸手办.png','手办','SSR','鬼灭之刃 手办周边，角色/主题：灶门炭治郎水之呼吸手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:09:17.468009','exchange_published',520,260,NULL,44,5),(53,'2026-06-08 11:23:17.494778','2026-06-08 11:23:17.507964','炭治郎日轮刀模型','/media/product/炭治郎日轮刀模型.png','手办','SSR','鬼灭之刃 手办周边，角色/主题：炭治郎日轮刀模型。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:07:17.468009','exchange_published',520,260,NULL,45,5),(54,'2026-06-08 11:23:17.494778','2026-06-08 11:23:17.507964','爱蜜莉雅雪花手办','/media/product/爱蜜莉雅雪花手办.png','手办','SSR','综合动漫 手办周边，角色/主题：爱蜜莉雅雪花手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:05:17.468009','exchange_published',520,260,NULL,46,5),(55,'2026-06-08 11:23:17.495806','2026-06-08 11:23:17.495806','牧濑红莉栖实验室手办','/media/product/牧濑红莉栖实验室手办.png','手办','SSR','综合动漫 手办周边，角色/主题：牧濑红莉栖实验室手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:03:17.468009','available',520,260,NULL,47,5),(56,'2026-06-08 11:23:17.495806','2026-06-08 11:23:17.495806','由比滨结衣亚克力挂件','/media/product/由比滨结衣亚克力挂件.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：由比滨结衣亚克力挂件。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 11:01:17.468009','available',300,150,NULL,48,5),(57,'2026-06-08 11:23:17.496777','2026-06-08 11:23:17.496777','电次电锯形态手办','/media/product/电次电锯形态手办.png','手办','SSR','综合动漫 手办周边，角色/主题：电次电锯形态手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 10:59:17.468009','available',520,260,NULL,49,5),(58,'2026-06-08 11:23:17.496777','2026-06-08 11:23:17.496777','皮卡丘毛绒玩偶','/media/product/皮卡丘毛绒玩偶.png','毛绒','R','宝可梦 毛绒周边，角色/主题：皮卡丘毛绒玩偶。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 10:57:17.468009','available',160,80,NULL,50,5),(59,'2026-06-08 11:23:17.497282','2026-06-08 11:23:17.497282','祢豆子竹筒玩偶','/media/product/祢豆子竹筒玩偶.png','毛绒','R','鬼灭之刃 毛绒周边，角色/主题：祢豆子竹筒玩偶。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 10:55:17.468009','available',160,80,NULL,51,5),(60,'2026-06-08 11:23:17.497282','2026-06-08 11:23:17.497282','空条承太郎白金之星手办','/media/product/空条承太郎白金之星手办.png','手办','SSR','JOJO 手办周边，角色/主题：空条承太郎白金之星手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 10:53:17.468009','available',520,260,NULL,52,5),(61,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','索隆三刀流亚克力','/media/product/索隆三刀流亚克力.png','亚克力','SR','海贼王 亚克力周边，角色/主题：索隆三刀流亚克力。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 10:51:17.468009','available',300,150,NULL,53,5),(62,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','约尔亚克力','/media/product/约尔亚克力.png','亚克力','SR','综合动漫 亚克力周边，角色/主题：约尔亚克力。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 10:49:17.468009','available',300,150,NULL,54,5),(63,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','纳西妲立牌','/media/product/纳西妲立牌.png','亚克力','SR','原神 亚克力周边，角色/主题：纳西妲立牌。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 10:47:17.468009','available',300,150,NULL,55,5),(64,'2026-06-08 11:23:17.498291','2026-06-08 11:23:17.498291','绫波丽白色驾驶服手办','/media/product/绫波丽白色驾驶服手办.png','手办','SSR','EVA 手办周边，角色/主题：绫波丽白色驾驶服手办。用于P3盲盒抽取、我的资产和换物测试。','blindbox','P3_REAL 换物市场测试','2026-06-08 10:45:17.468009','available',520,260,NULL,56,5),(65,'2026-06-08 11:27:24.489626','2026-06-08 11:27:24.489626','明日香红色驾驶服手办','/media/product/明日香红色驾驶服手办.png','IP主题盲盒','SSR','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',520,260,NULL,33,4),(66,'2026-06-08 11:27:24.498719','2026-06-08 11:27:24.498719','明日香限定卡片','/media/product/明日香限定卡片.png','IP主题盲盒','SR','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',300,150,NULL,34,4),(67,'2026-06-08 11:27:24.500718','2026-06-08 11:27:24.500718','明日香限定卡片','/media/product/明日香限定卡片.png','IP主题盲盒','SR','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',300,150,NULL,34,4),(68,'2026-06-08 11:27:24.502230','2026-06-08 11:27:24.502230','明日香限定卡片','/media/product/明日香限定卡片.png','IP主题盲盒','SR','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',300,150,NULL,34,4),(69,'2026-06-08 11:27:24.507866','2026-06-08 11:27:24.507866','初号机金属徽章','/media/product/初号机金属徽章.png','IP主题盲盒','SR','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',300,150,NULL,16,4),(70,'2026-06-08 11:27:24.510875','2026-06-08 11:27:24.510875','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','IP主题盲盒','R','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',160,80,NULL,1,4),(71,'2026-06-08 11:27:24.514991','2026-06-08 11:27:24.514991','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','IP主题盲盒','R','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',160,80,NULL,1,4),(72,'2026-06-08 11:27:24.518502','2026-06-08 11:27:24.518502','绫波丽白色驾驶服手办','/media/product/绫波丽白色驾驶服手办.png','IP主题盲盒','SSR','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',520,260,NULL,56,4),(73,'2026-06-08 11:27:24.521737','2026-06-08 11:27:24.521737','EVA 机体设定海报','/media/product/EVA 机体设定海报.png','IP主题盲盒','R','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',160,80,NULL,1,4),(74,'2026-06-08 11:27:24.524294','2026-06-08 11:27:24.524294','绫波丽白色驾驶服手办','/media/product/绫波丽白色驾驶服手办.png','IP主题盲盒','SSR','来自P3真实EVA主题盲盒','blindbox','P3真实EVA主题盲盒','2026-06-08 11:27:24.488681','recycled',520,260,NULL,56,4);
/*!40000 ALTER TABLE `user_asset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'Web'
--

--
-- Dumping routines for database 'Web'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-08 19:28:14
