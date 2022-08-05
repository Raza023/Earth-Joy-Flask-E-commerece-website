-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: earthjoy
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `adminId` int NOT NULL AUTO_INCREMENT,
  `adminName` varchar(50) NOT NULL,
  `adminEmail` varchar(45) NOT NULL,
  `adminPswd` varchar(50) NOT NULL,
  `adminGender` varchar(10) NOT NULL,
  `adminAddress` varchar(100) NOT NULL,
  PRIMARY KEY (`adminId`),
  UNIQUE KEY `adminId_UNIQUE` (`adminId`),
  UNIQUE KEY `adminEmail_UNIQUE` (`adminEmail`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'admin','admin@gmail.com','adminbhai','male','lahore');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buyer`
--

DROP TABLE IF EXISTS `buyer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buyer` (
  `buyerId` int NOT NULL AUTO_INCREMENT,
  `buyerName` varchar(45) NOT NULL,
  `buyerEmail` varchar(50) NOT NULL,
  `buyerGender` varchar(10) NOT NULL,
  `buyerDOB` varchar(50) NOT NULL,
  `buyerPswd` varchar(50) NOT NULL,
  `buyerPic` varchar(45) NOT NULL,
  PRIMARY KEY (`buyerId`),
  UNIQUE KEY `buyerId_UNIQUE` (`buyerId`),
  UNIQUE KEY `buyerEmail_UNIQUE` (`buyerEmail`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buyer`
--

LOCK TABLES `buyer` WRITE;
/*!40000 ALTER TABLE `buyer` DISABLE KEYS */;
INSERT INTO `buyer` VALUES (1,'Hassan','hassan@gmail.con','Male','2000-12-12','123456789','1.png'),(2,'Haider','haider@gmail.com','Male','2000-12-12','123456789','2.png'),(3,'Farhan','farhan@gmail.com','Male','2000-12-12','123456789','3.png'),(4,'Hassan Raza','hr770735@gmail.com','Male','2000-12-12','123456789','4.png');
/*!40000 ALTER TABLE `buyer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `cartId` int NOT NULL AUTO_INCREMENT,
  `byrid` int NOT NULL,
  `ChkOutStatus` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`cartId`),
  UNIQUE KEY `cartId_UNIQUE` (`cartId`),
  KEY `bid_idx` (`byrid`),
  CONSTRAINT `byrid` FOREIGN KEY (`byrid`) REFERENCES `buyer` (`buyerId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,1,0),(2,2,0),(3,3,0),(4,4,0);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cartproduct`
--

DROP TABLE IF EXISTS `cartproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cartproduct` (
  `cid` int DEFAULT NULL,
  `productId` int DEFAULT NULL,
  `prdQuantity` int DEFAULT '0',
  `cpid` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`cpid`),
  UNIQUE KEY `cpid_UNIQUE` (`cpid`),
  KEY `cid_idx` (`cid`),
  KEY `productId_idx` (`productId`),
  CONSTRAINT `cid` FOREIGN KEY (`cid`) REFERENCES `cart` (`cartId`),
  CONSTRAINT `productId` FOREIGN KEY (`productId`) REFERENCES `products` (`productId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cartproduct`
--

LOCK TABLES `cartproduct` WRITE;
/*!40000 ALTER TABLE `cartproduct` DISABLE KEYS */;
INSERT INTO `cartproduct` VALUES (1,1,3,1),(1,2,2,2),(1,3,2,3),(2,2,3,4);
/*!40000 ALTER TABLE `cartproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `catID` int NOT NULL AUTO_INCREMENT,
  `categoryName` varchar(45) NOT NULL,
  PRIMARY KEY (`catID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Electronic devices'),(2,'Home Appliances'),(3,'Health & Beauty'),(4,'Groceries'),(5,'Fashon'),(6,'Automobile');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `checkout`
--

DROP TABLE IF EXISTS `checkout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `checkout` (
  `chkid` int NOT NULL AUTO_INCREMENT,
  `cartId` int NOT NULL,
  `cartDate` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `deliveryStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`chkid`),
  UNIQUE KEY `chkid_UNIQUE` (`chkid`),
  KEY `cartId_idx` (`cartId`),
  CONSTRAINT `cartId` FOREIGN KEY (`cartId`) REFERENCES `cart` (`cartId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checkout`
--

LOCK TABLES `checkout` WRITE;
/*!40000 ALTER TABLE `checkout` DISABLE KEYS */;
INSERT INTO `checkout` VALUES (1,1,'12-12-2021','Lahore Bandian ala Pul','pending'),(2,2,'01-01-2022','Kashmir ','Delivered');
/*!40000 ALTER TABLE `checkout` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favourite`
--

DROP TABLE IF EXISTS `favourite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favourite` (
  `fId` int NOT NULL AUTO_INCREMENT,
  `bId` int NOT NULL,
  `pId` int NOT NULL,
  PRIMARY KEY (`fId`),
  UNIQUE KEY `fId_UNIQUE` (`fId`),
  KEY `bId_idx` (`bId`),
  KEY `pId_idx` (`pId`),
  CONSTRAINT `bId` FOREIGN KEY (`bId`) REFERENCES `buyer` (`buyerId`),
  CONSTRAINT `pId` FOREIGN KEY (`pId`) REFERENCES `products` (`productId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favourite`
--

LOCK TABLES `favourite` WRITE;
/*!40000 ALTER TABLE `favourite` DISABLE KEYS */;
/*!40000 ALTER TABLE `favourite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `mId` int NOT NULL AUTO_INCREMENT,
  `message` varchar(200) NOT NULL,
  `dateTime` varchar(50) NOT NULL,
  `messageby` varchar(45) NOT NULL,
  PRIMARY KEY (`mId`),
  UNIQUE KEY `mId_UNIQUE` (`mId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `productId` int NOT NULL AUTO_INCREMENT,
  `pName` varchar(100) NOT NULL,
  `pType` varchar(45) NOT NULL,
  `pDescription` varchar(500) NOT NULL,
  `pPrice` double NOT NULL,
  `pStock` int NOT NULL,
  `pMainTag` varchar(100) NOT NULL,
  `pImages` varchar(45) NOT NULL,
  `pAppStatus` tinyint NOT NULL DEFAULT '0',
  `sellerId` int NOT NULL,
  `aId` int DEFAULT NULL,
  `pClick` int NOT NULL DEFAULT '0',
  `pblockStatus` tinyint(1) DEFAULT '0',
  `proDel` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`productId`),
  UNIQUE KEY `productId_UNIQUE` (`productId`),
  KEY `sellerId_idx` (`sellerId`),
  KEY `adminId_idx` (`aId`),
  CONSTRAINT `aId` FOREIGN KEY (`aId`) REFERENCES `admin` (`adminId`),
  CONSTRAINT `sellerId` FOREIGN KEY (`sellerId`) REFERENCES `seller` (`sellerId`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Vivo y21','Phones','Made in Pakistan',75000,23,'Lets change the game','1.jpg',1,1,1,12,0,0),(2,'Huawei Mate 40 Pro','Phones','Made in Pakistan',85000,12,'Huawei Mobiles','2.png',1,1,1,12,0,0),(3,'Xiomi Redmi 10','Phones','Made in China',90000,12,'Xiomi Mobiles','3.jpg',1,1,1,12,0,0),(4,'Samsung Y6','Tablets','Made in Pakistan',100000,14,'Samsung ','4.png',1,1,1,5,0,0),(5,'Huawei Global','Tablets','Made in Pakistan',80000,7,'Huawei Mobiles','5.jpg',1,1,1,6,0,0),(6,'Q Tab','Tablets','Made in Pakistan',40000,13,'Q Mobiles','6.jpg',1,1,1,10,0,0),(7,'Dell Latitude E5440','Laptops','Made in Pakistan',80000,23,'Dell LTD','7.jpg',1,1,1,12,0,0),(8,'Lenovo 3S','Laptops','Made in Pakistan',60000,7,'Lenovo LTD','8.jpg',1,1,1,13,0,0),(9,'Dell DS4','Desktop','Made in Pakistan',70000,10,'Dell LTD','9.jpg',1,1,1,7,0,0),(10,'HP 4S','Desktop','Made in Pakistan',40000,12,'HP LTD','10.jpg',1,1,1,2,0,0),(11,'Nokia Camera','Cameras & Drones','Made in Japan',50000,4,'Nokia Company','11.jpg',1,1,1,2,0,0),(12,'Samsung Drone','Cameras & Drones','Made in Pakistan',100000,13,'Samsung Mobiles','12.jpg',1,1,1,2,0,0),(13,'Roku Watch','Smart Watches','Made in Pakistan',20000,20,'Dream Watch','13.jpg',1,1,1,7,0,0),(14,'XBOX','Gaming Consoles','Made in Pakistan',60000,12,'Gaming Masterio','14.jpg',1,1,1,18,0,0),(15,'PS4','Gaming Consoles','Made in Japan',20000,15,'Lets Play it.','15.jpg',1,1,1,12,0,0),(16,'Samsung LED','Smart TV','Made in Pakistan',20000,13,'Samsung','16.jpg',1,1,1,5,0,0),(17,'Haier LED','Smart TV','Made in China',10000,14,'Haier','17.jpg',1,1,1,9,0,0),(18,'Stereo Speaker','Home Audio','Made in Pakistan',5000,2,'Stereo','18.jpg',1,1,1,7,0,0),(19,'Presure Cooker','Kitchen Appliances','Made in Pakisttan',7000,3,'Enviro','19.jpg',1,1,1,7,0,0),(20,'Harpic Floor Cleaner','Floor Care','Made in Pakistan',200,100,'Harpic','20.jpg',1,1,1,8,0,0),(21,'Haier Generators','Generators','Made in Pakistan',1000,30,'Haier','21.jpg',1,1,1,6,0,0),(22,'Washing Machine','Washers & Dryers','Made in Pakistan',10000,12,'Enviro','22.jpg',1,1,1,10,0,0),(23,'Rose beauty Perfume','Fragrances','Made in Pakistan',5000,13,'Rose Beauty','23.jpg',1,1,1,9,0,0),(24,'Hair dryer','Hair Care','Made in Pakistan',2000,12,'Enviro','24.jpg',1,1,1,10,0,0),(25,'Beard Soap','Mens Care','Made in Pakistan',1000,13,'Darhi Mouch','25.jpg',1,1,1,13,0,0),(26,'Fair & Handsome','Skin Care','Made in Pakistan',300,9,'Fair & Handsome','26.jpg',1,1,1,12,0,0),(27,'Makeup kit','Makeup','Made in Pakisttan',500,21,'Bright & Beauty ','27.jpg',1,1,1,13,0,0),(28,'Drip set','Medical Supplies','Made in Korea',200,25,'Heuko','28.jpg',1,1,1,13,0,0),(29,'makeup machine','Beauty Tools','Made in Pakistan',400,24,'Bright & Beauty','29.jpg',1,1,1,12,0,0),(30,'coke 1.5 liters','Bevarages','Made in Pakistan',100,982,'Coca Cola','30.jpg',1,1,1,9,0,0),(31,'Cheese Cake','Fresh Products','Made in Pakistan',200,324,'Cakes & Bakes','31.jpg',1,1,1,14,0,0),(32,'Kurleez','Snacks','Made in Pakistan',30,2072,'Kurleez','32.jpg',1,1,1,15,0,0),(33,'Amm ka Muraba','Food Staples','Made in Lahore',100,34,'Bhai Muraba','33.jpg',1,1,1,14,0,0),(34,'Ice Browny','Dairy & Chilled','Made in Pakistan',120,600,'Chocolisious','34.jpg',1,1,1,23,0,0),(35,'Raho Fish','Frozen Food','Made in Pakistan',300,320,'Raho','35.jpg',1,1,1,34,0,0),(36,'Jeans pent','Mens Fashon','Made in Pakistan',200,289,'Addidas','36.jpg',1,1,1,23,0,0),(37,'Purse','Womens Fashon','Made in Pakistan',230,148,'Nike','37.jpg',1,1,1,14,0,0),(38,'Jacket','Winter Clothing','Made in Pakistan',212,345,'Addidas','38.jpg',1,1,1,14,0,0),(39,'T-Shirt','Summer Clothing','Made in Pakistan',200,398,'Addidas','39.jpg',1,1,1,14,0,0),(40,'Under wear','Inner wear','Made in Pakistan',100,540,'Nike','40.jpg',1,1,1,15,0,0),(41,'Sneaker','Shoes','Made in Pakistan',680,389,'Nike','41.jpg',1,1,1,18,0,0),(42,'Tires','Accessories','Made in China',240,356,'Pak Wheels','42.jpg',1,1,1,21,0,0),(43,'Honda 70','Motorcycles','Made in Pakistan',61000,23,'Honda','43.jpg',1,1,1,34,0,0),(44,'Honda Civic','Cars','Made in Pakistan',1000000,12,'Honda','44.jpg',1,1,1,46,0,0),(45,'Riksha - Yamaha','Rikshas','Made in China',45000,23,'Yamaha','45.jpg',1,1,1,47,0,0),(46,'Trackter','Loaders','Made in Pakistan',65000,25,'Yamaha','46.jpg',1,1,1,23,0,0),(47,'Heavy Bike','Sports Bikes','Made in Pakistan',900000,12,'Yamaha','47.jpg',1,1,1,29,0,0),(48,'Helmet','Helmets','Made in Pakistan',500,25,'Honda','48.jpg',1,1,1,32,0,0),(49,'Face Cover Mask','Riding Gears','Made in Pakistan',300,25,'H&S','49.jpg',1,1,1,47,0,0);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seller`
--

DROP TABLE IF EXISTS `seller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seller` (
  `sellerId` int NOT NULL AUTO_INCREMENT,
  `sellerName` varchar(45) NOT NULL,
  `sellerEmail` varchar(45) NOT NULL,
  `sellerPswd` varchar(45) NOT NULL,
  `sellerGender` varchar(45) NOT NULL,
  `sellerAddress` varchar(45) NOT NULL,
  `sellerCategory` varchar(45) NOT NULL,
  `AppStatus` tinyint NOT NULL DEFAULT '0',
  `sellerPic` varchar(45) NOT NULL,
  `adminId` int DEFAULT NULL,
  `blockStatus` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`sellerId`),
  UNIQUE KEY `sellerId_UNIQUE` (`sellerId`),
  UNIQUE KEY `sellerEmail_UNIQUE` (`sellerEmail`),
  KEY `adminId_idx` (`adminId`),
  CONSTRAINT `adminId` FOREIGN KEY (`adminId`) REFERENCES `admin` (`adminId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seller`
--

LOCK TABLES `seller` WRITE;
/*!40000 ALTER TABLE `seller` DISABLE KEYS */;
INSERT INTO `seller` VALUES (1,'Hassan Raza','hr770735@gmail.com','hassanbhai','male','Lahore Cantt','Electronics',1,'seller1',1,1),(2,'Hussain Raza','hr7770735@gmail.com','hussainbhai','male','Lahore Cantt','Furniture',1,'seller2',1,0),(3,'Ali Raza','hr7760735@gmail.com','alibhai','male','Lake City','Clothes',1,'seller3',1,0),(4,'Jawad Ali','jawad.ali@gmaiil.com','jawadbhai','male','Gujranwala','Furrniture',0,'seller4',1,0);
/*!40000 ALTER TABLE `seller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcategories`
--

DROP TABLE IF EXISTS `subcategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcategories` (
  `subcatid` int NOT NULL AUTO_INCREMENT,
  `catid` int NOT NULL,
  `subcategory` varchar(45) NOT NULL,
  PRIMARY KEY (`subcatid`),
  KEY `catid_idx` (`catid`),
  CONSTRAINT `catid` FOREIGN KEY (`catid`) REFERENCES `categories` (`catID`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategories`
--

LOCK TABLES `subcategories` WRITE;
/*!40000 ALTER TABLE `subcategories` DISABLE KEYS */;
INSERT INTO `subcategories` VALUES (1,1,'Phones'),(2,1,'Tablets'),(3,1,'Laptops'),(4,1,'Desktop'),(5,1,'Cameras & Drones'),(6,1,'Smart Watches'),(7,1,'Gaming Consoles'),(8,2,'Smart TV'),(9,2,'Home Audio'),(10,2,'Kitchen Appliances'),(11,2,'Cooling & Heating'),(12,2,'Floor Care'),(13,2,'Generators'),(14,2,'Washers & Dryers'),(15,3,'Fragrances'),(16,3,'Hair Care'),(17,3,'Mens Care'),(18,3,'Skin Care'),(19,3,'Medical Supplies'),(20,3,'Beauty Tools'),(21,4,'Bevarages'),(22,4,'Fresh Products'),(23,4,'Food Staples'),(24,4,'Dairy & Chilled'),(25,4,'Frozen Food'),(26,5,'Mens Fashon'),(27,5,'Womens Fashon'),(28,5,'Winter Clothing'),(29,5,'Summer Clothing'),(30,5,'Inner Wear'),(31,5,'Shoes'),(32,6,'Accessories'),(33,6,'Motocycles'),(34,6,'Cars'),(35,6,'Rikshas'),(36,6,'Loaders'),(37,6,'Sports Bikes'),(38,6,'Helmets'),(39,6,'Riding Gears');
/*!40000 ALTER TABLE `subcategories` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-26  3:17:29
