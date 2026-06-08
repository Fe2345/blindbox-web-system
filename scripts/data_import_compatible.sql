/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.3-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: blindbox
-- ------------------------------------------------------
-- Server version	11.8.3-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
set autocommit=0;
REPLACE INTO `accounts_user` VALUES
(1,'pbkdf2_sha256$1200000$netW4GiGUB9Qclivj8rGqd$H+vSva0vyjdPuB5QUMYsZtvAjESuEReXui54WLsYC/0=',NULL,0,'111','','','',0,1,'2026-05-29 06:12:39.981385','user','18301108746',''),
(2,'pbkdf2_sha256$1200000$F4Cl1QNUsqlHrYdzFTix2H$OYAN5c5hUNy7G85rloWlTyn3NLjYUMZKGkGwIvVLDQI=',NULL,0,'testuser2','','','',0,1,'2026-05-29 06:27:28.524985','user','13800000002',''),
(3,'pbkdf2_sha256$1200000$3zPsVup8qPq9LLI5XVHVyD$Clv6pjS1Q+1pqTURPSwrUxraBdNrgVxyP9awkwuCPUI=',NULL,0,'paimon','','','',0,1,'2026-06-03 07:21:03.161932','user','18301108746','/media/avatar/d5ad39290a3041a1896892812d30f655.png');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
REPLACE INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',3,'add_permission'),
(6,'Can change permission',3,'change_permission'),
(7,'Can delete permission',3,'delete_permission'),
(8,'Can view permission',3,'view_permission'),
(9,'Can add group',2,'add_group'),
(10,'Can change group',2,'change_group'),
(11,'Can delete group',2,'delete_group'),
(12,'Can view group',2,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add Token',6,'add_token'),
(22,'Can change Token',6,'change_token'),
(23,'Can delete Token',6,'delete_token'),
(24,'Can view Token',6,'view_token'),
(25,'Can add Token',7,'add_tokenproxy'),
(26,'Can change Token',7,'change_tokenproxy'),
(27,'Can delete Token',7,'delete_tokenproxy'),
(28,'Can view Token',7,'view_tokenproxy'),
(29,'Can add 鐢ㄦ埛',10,'add_user'),
(30,'Can change 鐢ㄦ埛',10,'change_user'),
(31,'Can delete 鐢ㄦ埛',10,'delete_user'),
(32,'Can view 鐢ㄦ埛',10,'view_user'),
(33,'Can add 琛屾斂鍖哄垝',9,'add_division'),
(34,'Can change 琛屾斂鍖哄垝',9,'change_division'),
(35,'Can delete 琛屾斂鍖哄垝',9,'delete_division'),
(36,'Can view 琛屾斂鍖哄垝',9,'view_division'),
(37,'Can add 鏀惰揣鍦板潃',8,'add_address'),
(38,'Can change 鏀惰揣鍦板潃',8,'change_address'),
(39,'Can delete 鏀惰揣鍦板潃',8,'delete_address'),
(40,'Can view 鏀惰揣鍦板潃',8,'view_address'),
(41,'Can add 鐩茬洅',11,'add_blindbox'),
(42,'Can change 鐩茬洅',11,'change_blindbox'),
(43,'Can delete 鐩茬洅',11,'delete_blindbox'),
(44,'Can view 鐩茬洅',11,'view_blindbox'),
(45,'Can add 濂栧搧',13,'add_prize'),
(46,'Can change 濂栧搧',13,'change_prize'),
(47,'Can delete 濂栧搧',13,'delete_prize'),
(48,'Can view 濂栧搧',13,'view_prize'),
(49,'Can add 鎶界洅璁板綍',12,'add_drawrecord'),
(50,'Can change 鎶界洅璁板綍',12,'change_drawrecord'),
(51,'Can delete 鎶界洅璁板綍',12,'delete_drawrecord'),
(52,'Can view 鎶界洅璁板綍',12,'view_drawrecord'),
(53,'Can add 鐢ㄦ埛璧勪骇',14,'add_asset'),
(54,'Can change 鐢ㄦ埛璧勪骇',14,'change_asset'),
(55,'Can delete 鐢ㄦ埛璧勪骇',14,'delete_asset'),
(56,'Can view 鐢ㄦ埛璧勪骇',14,'view_asset'),
(57,'Can add 璁㈠崟',15,'add_order'),
(58,'Can change 璁㈠崟',15,'change_order'),
(59,'Can delete 璁㈠崟',15,'delete_order'),
(60,'Can view 璁㈠崟',15,'view_order'),
(61,'Can add 鎹㈢墿甯栧瓙',17,'add_exchangepost'),
(62,'Can change 鎹㈢墿甯栧瓙',17,'change_exchangepost'),
(63,'Can delete 鎹㈢墿甯栧瓙',17,'delete_exchangepost'),
(64,'Can view 鎹㈢墿甯栧瓙',17,'view_exchangepost'),
(65,'Can add 鎹㈢墿鐢宠',16,'add_exchangeapplication'),
(66,'Can change 鎹㈢墿鐢宠',16,'change_exchangeapplication'),
(67,'Can delete 鎹㈢墿鐢宠',16,'delete_exchangeapplication'),
(68,'Can view 鎹㈢墿鐢宠',16,'view_exchangeapplication'),
(69,'Can add 绉垎璐︽埛',18,'add_pointsaccount'),
(70,'Can change 绉垎璐︽埛',18,'change_pointsaccount'),
(71,'Can delete 绉垎璐︽埛',18,'delete_pointsaccount'),
(72,'Can view 绉垎璐︽埛',18,'view_pointsaccount'),
(73,'Can add 绉垎娴佹按',19,'add_pointsrecord'),
(74,'Can change 绉垎娴佹按',19,'change_pointsrecord'),
(75,'Can delete 绉垎娴佹按',19,'delete_pointsrecord'),
(76,'Can view 绉垎娴佹按',19,'view_pointsrecord'),
(77,'Can add 浜ゆ槗璁板綍',20,'add_transactionrecord'),
(78,'Can change 浜ゆ槗璁板綍',20,'change_transactionrecord'),
(79,'Can delete 浜ゆ槗璁板綍',20,'delete_transactionrecord'),
(80,'Can view 浜ゆ槗璁板綍',20,'view_transactionrecord'),
(81,'Can add 鍟嗗',23,'add_merchant'),
(82,'Can change 鍟嗗',23,'change_merchant'),
(83,'Can delete 鍟嗗',23,'delete_merchant'),
(84,'Can view 鍟嗗',23,'view_merchant'),
(85,'Can add 鍟嗗鍟嗗搧',24,'add_product'),
(86,'Can change 鍟嗗鍟嗗搧',24,'change_product'),
(87,'Can delete 鍟嗗鍟嗗搧',24,'delete_product'),
(88,'Can view 鍟嗗鍟嗗搧',24,'view_product'),
(89,'Can add 搴撳瓨鍙樺姩璁板綍',22,'add_inventoryrecord'),
(90,'Can change 搴撳瓨鍙樺姩璁板綍',22,'change_inventoryrecord'),
(91,'Can delete 搴撳瓨鍙樺姩璁板綍',22,'delete_inventoryrecord'),
(92,'Can view 搴撳瓨鍙樺姩璁板綍',22,'view_inventoryrecord'),
(93,'Can add 搴撳瓨',21,'add_inventory'),
(94,'Can change 搴撳瓨',21,'change_inventory'),
(95,'Can delete 搴撳瓨',21,'delete_inventory'),
(96,'Can view 搴撳瓨',21,'view_inventory'),
(97,'Can add 鍙戣揣浠诲姟',25,'add_shipmenttask'),
(98,'Can change 鍙戣揣浠诲姟',25,'change_shipmenttask'),
(99,'Can delete 鍙戣揣浠诲姟',25,'delete_shipmenttask'),
(100,'Can view 鍙戣揣浠诲姟',25,'view_shipmenttask'),
(101,'Can add 寮傚父宸ュ崟',26,'add_exceptionrecord'),
(102,'Can change 寮傚父宸ュ崟',26,'change_exceptionrecord'),
(103,'Can delete 寮傚父宸ュ崟',26,'delete_exceptionrecord'),
(104,'Can view 寮傚父宸ュ崟',26,'view_exceptionrecord'),
(105,'Can add 鎿嶄綔鏃ュ織',27,'add_oplog'),
(106,'Can change 鎿嶄綔鏃ュ織',27,'change_oplog'),
(107,'Can delete 鎿嶄綔鏃ュ織',27,'delete_oplog'),
(108,'Can view 鎿嶄綔鏃ュ織',27,'view_oplog'),
(109,'Can add 瑙勫垯閰嶇疆',28,'add_ruleconfig'),
(110,'Can change 瑙勫垯閰嶇疆',28,'change_ruleconfig'),
(111,'Can delete 瑙勫垯閰嶇疆',28,'delete_ruleconfig'),
(112,'Can view 瑙勫垯閰嶇疆',28,'view_ruleconfig'),
(113,'Can add 浜ゆ槗璐︽湰',29,'add_transactionledger'),
(114,'Can change 浜ゆ槗璐︽湰',29,'change_transactionledger'),
(115,'Can delete 浜ゆ槗璐︽湰',29,'delete_transactionledger'),
(116,'Can view 浜ゆ槗璐︽湰',29,'view_transactionledger');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--

--
-- Dumping data for table `blindbox`
--

LOCK TABLES `blindbox` WRITE;
/*!40000 ALTER TABLE `blindbox` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `blindbox` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `blindbox_draw_record`
--

LOCK TABLES `blindbox_draw_record` WRITE;
/*!40000 ALTER TABLE `blindbox_draw_record` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `blindbox_draw_record` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `blindbox_prize`
--

LOCK TABLES `blindbox_prize` WRITE;
/*!40000 ALTER TABLE `blindbox_prize` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `blindbox_prize` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
REPLACE INTO `django_content_type` VALUES
(8,'accounts','address'),
(9,'accounts','division'),
(10,'accounts','user'),
(1,'admin','logentry'),
(14,'assets','asset'),
(2,'auth','group'),
(3,'auth','permission'),
(6,'authtoken','token'),
(7,'authtoken','tokenproxy'),
(11,'blindbox','blindbox'),
(12,'blindbox','drawrecord'),
(13,'blindbox','prize'),
(4,'contenttypes','contenttype'),
(16,'exchange','exchangeapplication'),
(17,'exchange','exchangepost'),
(21,'merchant','inventory'),
(22,'merchant','inventoryrecord'),
(23,'merchant','merchant'),
(24,'merchant','product'),
(25,'merchant','shipmenttask'),
(26,'operations','exceptionrecord'),
(27,'operations','oplog'),
(28,'operations','ruleconfig'),
(29,'operations','transactionledger'),
(15,'orders','order'),
(18,'points','pointsaccount'),
(19,'points','pointsrecord'),
(20,'points','transactionrecord'),
(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
REPLACE INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2026-05-29 01:25:18.224911'),
(2,'contenttypes','0002_remove_content_type_name','2026-05-29 01:25:18.255961'),
(3,'auth','0001_initial','2026-05-29 01:25:18.333023'),
(4,'auth','0002_alter_permission_name_max_length','2026-05-29 01:25:18.347601'),
(5,'auth','0003_alter_user_email_max_length','2026-05-29 01:25:18.350296'),
(6,'auth','0004_alter_user_username_opts','2026-05-29 01:25:18.352660'),
(7,'auth','0005_alter_user_last_login_null','2026-05-29 01:25:18.355015'),
(8,'auth','0006_require_contenttypes_0002','2026-05-29 01:25:18.356263'),
(9,'auth','0007_alter_validators_add_error_messages','2026-05-29 01:25:18.358335'),
(10,'auth','0008_alter_user_username_max_length','2026-05-29 01:25:18.360519'),
(11,'auth','0009_alter_user_last_name_max_length','2026-05-29 01:25:18.363124'),
(12,'auth','0010_alter_group_name_max_length','2026-05-29 01:25:18.372109'),
(13,'auth','0011_update_proxy_permissions','2026-05-29 01:25:18.376072'),
(14,'auth','0012_alter_user_first_name_max_length','2026-05-29 01:25:18.378388'),
(15,'accounts','0001_initial','2026-05-29 01:25:18.583948'),
(16,'admin','0001_initial','2026-05-29 01:25:18.621404'),
(17,'admin','0002_logentry_remove_auto_add','2026-05-29 01:25:18.625078'),
(18,'admin','0003_logentry_add_action_flag_choices','2026-05-29 01:25:18.629380'),
(19,'merchant','0001_initial','2026-05-29 01:25:18.752570'),
(20,'blindbox','0001_initial','2026-05-29 01:25:18.851164'),
(21,'assets','0001_initial','2026-05-29 01:25:18.906498'),
(22,'authtoken','0001_initial','2026-05-29 01:25:18.932250'),
(23,'authtoken','0002_auto_20160226_1747','2026-05-29 01:25:18.949375'),
(24,'authtoken','0003_tokenproxy','2026-05-29 01:25:18.951579'),
(25,'authtoken','0004_alter_tokenproxy_options','2026-05-29 01:25:18.954323'),
(26,'exchange','0001_initial','2026-05-29 01:25:19.047033'),
(27,'operations','0001_initial','2026-05-29 01:25:19.069220'),
(28,'orders','0001_initial','2026-05-29 01:25:19.113143'),
(29,'points','0001_initial','2026-05-29 01:25:19.190351'),
(30,'sessions','0001_initial','2026-05-29 01:25:19.206842'),
(31,'blindbox','0002_update_blindbox_prize_drawrecord','2026-06-01 13:56:13.921672');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `exception_record`
--

LOCK TABLES `exception_record` WRITE;
/*!40000 ALTER TABLE `exception_record` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `exception_record` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `exchange_application`
--

LOCK TABLES `exchange_application` WRITE;
/*!40000 ALTER TABLE `exchange_application` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `exchange_application` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `exchange_post`
--

LOCK TABLES `exchange_post` WRITE;
/*!40000 ALTER TABLE `exchange_post` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `exchange_post` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `merchant`
--

LOCK TABLES `merchant` WRITE;
/*!40000 ALTER TABLE `merchant` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `merchant` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `merchant_inventory`
--

LOCK TABLES `merchant_inventory` WRITE;
/*!40000 ALTER TABLE `merchant_inventory` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `merchant_inventory` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `merchant_inventory_record`
--

LOCK TABLES `merchant_inventory_record` WRITE;
/*!40000 ALTER TABLE `merchant_inventory_record` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `merchant_inventory_record` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `merchant_product`
--

LOCK TABLES `merchant_product` WRITE;
/*!40000 ALTER TABLE `merchant_product` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `merchant_product` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `merchant_shipment`
--

LOCK TABLES `merchant_shipment` WRITE;
/*!40000 ALTER TABLE `merchant_shipment` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `merchant_shipment` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `operation_log`
--

LOCK TABLES `operation_log` WRITE;
/*!40000 ALTER TABLE `operation_log` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `operation_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `points_account`
--

LOCK TABLES `points_account` WRITE;
/*!40000 ALTER TABLE `points_account` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `points_account` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `points_record`
--

LOCK TABLES `points_record` WRITE;
/*!40000 ALTER TABLE `points_record` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `points_record` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `rule_config`
--

LOCK TABLES `rule_config` WRITE;
/*!40000 ALTER TABLE `rule_config` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `rule_config` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `transaction_ledger`
--

LOCK TABLES `transaction_ledger` WRITE;
/*!40000 ALTER TABLE `transaction_ledger` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `transaction_ledger` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping data for table `transaction_record`
--

LOCK TABLES `transaction_record` WRITE;
/*!40000 ALTER TABLE `transaction_record` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `transaction_record` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--

--
-- Dumping data for table `user_asset`
--

LOCK TABLES `user_asset` WRITE;
/*!40000 ALTER TABLE `user_asset` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `user_asset` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-06-08  3:29:15
