-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_1682_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

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
-- Table structure for table `book_recives`
--

DROP TABLE IF EXISTS `book_recives`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_recives` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_book` int(11) NOT NULL,
  `id_users` int(11) NOT NULL,
  `mark` int(11) NOT NULL,
  `text` varchar(255) NOT NULL,
  `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_book` (`id_book`),
  KEY `id_users` (`id_users`),
  CONSTRAINT `book_recives_ibfk_1` FOREIGN KEY (`id_book`) REFERENCES `books` (`id`),
  CONSTRAINT `book_recives_ibfk_2` FOREIGN KEY (`id_users`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_recives`
--

LOCK TABLES `book_recives` WRITE;
/*!40000 ALTER TABLE `book_recives` DISABLE KEYS */;
/*!40000 ALTER TABLE `book_recives` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_book` varchar(225) NOT NULL,
  `short_description` text NOT NULL,
  `year` date NOT NULL,
  `publishing_house` varchar(25) NOT NULL,
  `author` varchar(225) NOT NULL,
  `volume` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8 COMMENT='Описание книги';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (27,'1984','Для подавления массовых волнений Океании правящая партия заново воссоздает прошлое и настоящее. За каждым гражданином неусыпно наблюдают, каждому с помощью телевидения промывают мозги. И даже двое любовников вынуждены скрывать свои чувства, поскольку секс и межличностные отношения объявлены вне закона.','1949-01-01','АСТ','Джордж Оруэлл',320),(30,'Искуство цвета','Автор разбирает закономерности цветовых контрастов, цветовой гармонии и цветового конструирования. Для художников, архитекторов и дизайнеров самых разнообразных сфер деятельности.','1961-01-01','Дмитрий Аронов','Иоганнес Иттен',96),(31,'Мастер и Маргарита','«Ма́стер и Маргари́та» — роман Михаила Афанасьевича Булгакова, работа над которым началась в декабре 1928 года и продолжалась вплоть до смерти писателя. Роман относится к незавершённым произведениям; редактирование и сведение воедино черновых записей осуществляла после смерти мужа вдова писателя — Елена Сергеевна.','1966-01-01','YMCA-Press','Михаил Булгаков',470),(34,'Маленький принц','«Ма́ленький принц» — аллегорическая повесть-сказка, наиболее известное произведение Антуана де Сент-Экзюпери. Сказка рассказывает о Маленьком принце, который посещает различные планеты в космосе, включая Землю. Книга обращается к темам одиночества, дружбы, любви и утраты.','1943-01-01','Дом Мещерякова.','Антуана де Сент-Экзюпери',160),(36,'Война и мир','«Война́ и мир» — роман-эпопея Льва Николаевича Толстого, описывающий русское общество в эпоху войн против Наполеона в 1805—1812 годах. Эпилог романа доводит повествование до 1820 года.','1843-01-01','Русский вестник',' Лев Николаевич Толстой',1300),(37,'О дивный новый мир','«О дивный новый мир» — антиутопический сатирический роман английского писателя Олдоса Хаксли, опубликованный в 1932 году. В заглавие вынесена строчка из трагикомедии: О чудо! Какое множество прекрасных лиц! Как род людской красив! И как хорош Тот новый мир, где есть такие люди! — Уильям Шекспир.','1932-01-01','Chatto &amp; Windus','Олдос Хаксли',352),(38,'Мы','«Мы» — фантастический роман-антиутопия Евгения Замятина с элементами сатиры, написанный в 1920 году. Действие разворачивается приблизительно в тридцать втором веке.','1924-01-01','Avon Publications','Евгений Замятин',208),(39,'451 градус по Фаренгейту','«451 градус по Фаренгейту» — научно-фантастический роман-антиутопия Рэя Брэдбери, изданный в 1953 году. Роман описывает американское общество близкого будущего, в котором книги находятся под запретом; «пожарные», к числу которых принадлежит и главный герой Гай Монтэг, сжигают любые найденные книги.','1953-01-01','Ballantine Books','Рэй Брэдбери',200),(40,'Заводной апельсин','«Заводно́й апельси́н» — роман Энтони Бёрджесса, написанный в 1962 году. Роман лёг в основу одноимённого фильма, снятого в 1971 году Стэнли Кубриком.','1962-01-01','Heinemann','Энтони Бёрджесс',200),(41,'Скотный двор','«Скотный двор» — изданная в 1945 году сатирическая повесть-притча Джорджа Оруэлла. В повести изображена эволюция общества животных, изгнавших со скотного двора его предыдущего владельца, жестокого мистера Джонса, от безграничной свободы к диктатуре свиньи по кличке Наполеон.','1945-01-01','Harvill Secker','Джордж Оруэлл',256);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `covers_books`
--

DROP TABLE IF EXISTS `covers_books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `covers_books` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(100) NOT NULL,
  `id_book` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `md5_hash` (`md5_hash`),
  KEY `id_book` (`id_book`),
  CONSTRAINT `covers_books_ibfk_1` FOREIGN KEY (`id_book`) REFERENCES `books` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `covers_books`
--

LOCK TABLES `covers_books` WRITE;
/*!40000 ALTER TABLE `covers_books` DISABLE KEYS */;
INSERT INTO `covers_books` VALUES ('3c0c5134-39d4-4787-a471-62fa4d2add41','5026192x.jpg','image/jpeg','8bd74254e5c86cbf9a5fe41e97f786bb',30),('47abace1-c73f-4d92-bf28-64fd36620d73','1023704112.jpg','image/jpeg','3182b03a5397abfda2d4d77afb8067f9',36),('48da89d6-3205-4f20-a776-7679deb53ba4','cover1__w340_2.jpg','image/jpeg','0aad1eed03a6e3b23b2a6353e6886a5a',40),('7ca09aeb-f03c-4667-8232-a5002a792c88','cover1__w340.jpg','image/jpeg','1fa448a019b93515a62fb596d82be467',27),('8185157e-8eb6-4ac5-9447-6f108657018b','39507162--.jpg','image/jpeg','8d24a4052e1963ad3475487322cc4bd6',39),('a0c17eb5-3d71-4d0e-824f-dddf993c3a29','boocover.jpg','image/jpeg','f273fad4e296b213370b97b8e2deba74',38),('ad6d3a32-10c2-491d-b157-689d54bd737e','10592409_0.jpg','image/jpeg','a32a216d34522f892a74f0497c93319c',41),('cce0eac0-7014-45e9-bda1-1a8008baf438','6252082701.jpg','image/jpeg','29ed0e4921a7773d47fc543989d87467',34),('e0c27685-7261-466a-be0a-0858e95c4455','cover1__w340_1.jpg','image/jpeg','8a44785708a1317c748306df6e4ed2ac',37),('f85d7a50-fd30-4f11-b5d6-1ed2b7725aa3','22311873-mihail-bulgakov-master-i-margarita-kollekcionnoe-illustrirovannoe-22311873.jpg','image/jpeg','1b26cd9e3225c3cc95e2395cb297fa31',31);
/*!40000 ALTER TABLE `covers_books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genrys`
--

DROP TABLE IF EXISTS `genrys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genrys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `genry` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='Жанры книг';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genrys`
--

LOCK TABLES `genrys` WRITE;
/*!40000 ALTER TABLE `genrys` DISABLE KEYS */;
INSERT INTO `genrys` VALUES (1,'Детектив'),(9,'Дизайн'),(2,'Драма'),(8,'Литература'),(6,'Мистика'),(4,'Приключения'),(3,'Роман'),(7,'Фантастика'),(5,'Фэнтези ');
/*!40000 ALTER TABLE `genrys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genrys_books`
--

DROP TABLE IF EXISTS `genrys_books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genrys_books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_book` int(11) NOT NULL,
  `id_genry` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_book` (`id_book`),
  KEY `id_genry` (`id_genry`),
  CONSTRAINT `genrys_books_ibfk_1` FOREIGN KEY (`id_book`) REFERENCES `books` (`id`),
  CONSTRAINT `genrys_books_ibfk_2` FOREIGN KEY (`id_genry`) REFERENCES `genrys` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genrys_books`
--

LOCK TABLES `genrys_books` WRITE;
/*!40000 ALTER TABLE `genrys_books` DISABLE KEYS */;
INSERT INTO `genrys_books` VALUES (39,27,5),(42,30,9),(43,31,3),(46,34,7),(48,36,6),(49,37,8),(50,38,8),(51,39,8),(52,40,8),(53,41,8);
/*!40000 ALTER TABLE `genrys_books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Администратор','суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'Модератор','может редактировать данные книг и производить модерацию рецензий'),(3,'Пользователь ','может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(25) NOT NULL,
  `first_name` varchar(25) NOT NULL,
  `last_name` varchar(25) NOT NULL,
  `middle_name` varchar(25) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `password_hash` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (7,'admin','Ренат','Рахматуллаев','Русланович',1,'pbkdf2:sha256:260000$svhrN9ZNQ2k4VKsc$dc4753515c149eb01a6ed9e2f5af5ddb4ffe622c533613183ae88c9fe244cf03'),(16,'renat','Ренат','Рахматуллаев','Русланович',1,'pbkdf2:sha256:260000$KU5xVHWqiMtqtqlZ$e1bdb455292c320385e0a277c3099711d663419c3a145e9f6423bec405b705e3');
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

-- Dump completed on 2022-06-24 13:36:24
