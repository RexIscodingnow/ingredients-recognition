CREATE DATABASE  IF NOT EXISTS `recipes_ingredients` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `recipes_ingredients`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: recipes_ingredients
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients` (
  `ingredient_id` int NOT NULL AUTO_INCREMENT,
  `ingredient_name` varchar(20) NOT NULL,
  PRIMARY KEY (`ingredient_id`),
  UNIQUE KEY `ingredient_name` (`ingredient_name`)
) ENGINE=InnoDB AUTO_INCREMENT=305 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (38,'九層塔'),(288,'冬粉'),(48,'味精'),(56,'大蒜'),(42,'大辣椒'),(273,'嫩豆腐'),(40,'小黃瓜'),(39,'川耳(泡發)'),(287,'彩椒'),(281,'木耳'),(295,'杏鮑菇'),(298,'櫛瓜'),(280,'水'),(277,'油'),(290,'牛肉'),(301,'玉米'),(275,'生抽'),(270,'番茄'),(43,'白芝麻'),(292,'白蘿蔔'),(46,'白醋'),(47,'砂糖'),(296,'碗豆'),(291,'秋葵'),(34,'米酒'),(35,'糖'),(269,'紅蘿蔔'),(274,'絞肉'),(57,'胡椒'),(302,'芹菜'),(279,'苦瓜'),(271,'茄子'),(285,'菠菜'),(284,'蒜'),(41,'蒜末'),(36,'蒜頭'),(55,'蔥'),(52,'蔥花'),(49,'蕃茄'),(51,'蕃茄醬'),(37,'薑'),(272,'薑片'),(282,'蠔油'),(303,'豆腐'),(54,'豬五花'),(293,'豬肉'),(59,'豬肉絲'),(300,'辣椒'),(33,'醬油'),(44,'醬油膏'),(278,'金針菇'),(31,'雞扒/雞排'),(304,'雞肉'),(50,'雞蛋'),(58,'青椒'),(283,'青江菜'),(45,'香油'),(276,'香菇'),(297,'馬鈴薯'),(299,'高麗菜'),(294,'鴻喜菇'),(286,'鹽'),(53,'鹽巴'),(32,'麻油'),(289,'黑木耳');
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe_ratings`
--

DROP TABLE IF EXISTS `recipe_ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe_ratings` (
  `user_id` int NOT NULL,
  `recipe_id` int NOT NULL,
  `rating` int NOT NULL,
  PRIMARY KEY (`user_id`,`recipe_id`),
  KEY `recipe_id` (`recipe_id`),
  CONSTRAINT `recipe_ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `recipe_ratings_ibfk_2` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`recipe_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe_ratings`
--

LOCK TABLES `recipe_ratings` WRITE;
/*!40000 ALTER TABLE `recipe_ratings` DISABLE KEYS */;
INSERT INTO `recipe_ratings` VALUES (8,1,5),(8,3,2),(8,4,4),(8,7,1),(8,8,2),(8,9,2),(8,14,4),(8,40,3),(9,1,2),(9,2,1),(9,6,2),(9,9,2),(9,10,2),(9,14,4),(9,21,4),(9,22,2),(9,39,5),(9,47,3),(9,51,3),(11,1,5),(11,2,2),(11,6,2),(11,9,2),(11,10,3),(11,11,2),(11,12,1),(11,14,5),(11,15,4),(11,21,1),(11,23,2),(11,24,2),(11,37,2),(11,38,4),(11,40,2),(11,48,4),(11,49,3),(11,50,5),(12,2,2),(12,4,4),(12,5,4),(12,7,1),(12,8,2),(12,10,2),(12,12,2),(12,14,4),(12,15,3),(12,21,2),(12,24,3),(12,37,2),(12,38,3),(12,39,4),(12,40,2),(12,47,3),(12,48,5),(12,50,4),(13,4,1),(13,5,1),(13,6,4),(13,8,5),(13,10,2),(13,11,3),(13,23,4),(13,24,4),(13,39,2),(13,47,4),(13,48,1),(13,50,2),(13,51,3),(14,1,5),(14,2,1),(14,4,4),(14,6,4),(14,7,3),(14,9,2),(14,11,1),(14,12,2),(14,14,4),(14,21,3),(14,22,5),(14,23,2),(14,37,2),(14,38,3),(14,39,5),(14,40,4),(14,48,5),(14,50,5),(14,51,4),(15,1,3),(15,7,2),(15,11,2),(15,13,3),(15,14,4),(15,15,3),(15,21,2),(15,23,2),(15,38,3),(15,39,4),(15,49,1),(16,1,5),(16,4,5),(16,5,5),(16,6,3),(16,8,2),(16,9,2),(16,10,1),(16,13,3),(16,14,2),(16,15,2),(16,21,2),(16,22,3),(16,47,3),(16,48,4),(16,49,1),(17,2,2),(17,4,5),(17,6,4),(17,7,1),(17,11,1),(17,13,3),(17,14,4),(17,21,2),(17,23,2),(17,24,3),(17,38,3),(17,39,5),(17,40,3),(17,47,4),(17,48,5),(17,49,2),(17,50,4),(17,51,2),(18,3,4),(18,5,5),(18,6,4),(18,7,1),(18,9,1),(18,11,3),(18,12,2),(18,13,2),(18,15,4),(18,24,3),(18,37,2),(18,39,5),(18,40,3),(18,47,4),(19,2,3),(19,4,2),(19,5,3),(19,7,4),(19,8,2),(19,10,1),(19,13,2),(19,14,3),(19,15,2),(19,22,3),(19,40,4),(19,49,3),(19,50,4);
/*!40000 ALTER TABLE `recipe_ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipeingredients`
--

DROP TABLE IF EXISTS `recipeingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipeingredients` (
  `recipe_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  PRIMARY KEY (`recipe_id`,`ingredient_id`),
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `recipeingredients_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`recipe_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `recipeingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipeingredients`
--

LOCK TABLES `recipeingredients` WRITE;
/*!40000 ALTER TABLE `recipeingredients` DISABLE KEYS */;
INSERT INTO `recipeingredients` VALUES (1,31),(1,32),(40,32),(1,33),(4,33),(5,33),(8,33),(9,33),(10,33),(40,33),(48,33),(1,34),(4,34),(1,35),(3,35),(4,35),(10,35),(11,35),(1,36),(5,36),(13,36),(21,36),(37,36),(39,36),(40,36),(47,36),(48,36),(49,36),(50,36),(51,36),(1,37),(23,37),(1,38),(2,39),(2,40),(11,40),(2,41),(11,41),(12,41),(2,42),(2,43),(2,44),(2,45),(4,45),(8,45),(9,45),(2,46),(2,47),(2,48),(3,49),(12,49),(3,50),(6,50),(7,50),(9,50),(15,50),(22,50),(38,50),(3,51),(3,52),(3,53),(4,53),(5,53),(4,54),(4,55),(8,55),(9,55),(4,56),(4,57),(7,57),(9,57),(13,57),(15,57),(5,58),(5,59),(9,269),(6,270),(10,271),(51,271),(10,272),(39,272),(40,272),(50,272),(8,273),(10,274),(10,275),(8,276),(9,276),(6,277),(7,277),(12,277),(13,277),(15,277),(8,278),(7,279),(10,280),(14,280),(9,281),(10,282),(8,283),(12,283),(6,284),(8,284),(9,284),(10,284),(6,285),(6,286),(7,286),(11,286),(12,286),(13,286),(14,286),(15,286),(21,286),(22,286),(23,286),(24,286),(37,286),(38,286),(47,286),(49,286),(50,286),(51,286),(10,287),(9,288);
/*!40000 ALTER TABLE `recipeingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipes` (
  `recipe_id` int NOT NULL AUTO_INCREMENT,
  `recipe_name` varchar(20) NOT NULL,
  `recipe_info_url` text,
  `cooking_step` text,
  PRIMARY KEY (`recipe_id`),
  UNIQUE KEY `recipe_name` (`recipe_name`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipes`
--

LOCK TABLES `recipes` WRITE;
/*!40000 ALTER TABLE `recipes` DISABLE KEYS */;
INSERT INTO `recipes` VALUES (1,'台式三杯雞','','備料:\r\n雞扒/雞排    2塊\r\n麻油         2湯匙\r\n醬油         2湯匙\r\n米酒         2湯匙\r\n糖           1/2湯匙\r\n蒜頭         3瓣\r\n薑           2片\r\n九層塔       1 束\r\n\r\n步驟:\r\n1. 蒜頭切片\r\n2. 中火熱鍋煎雞扒/雞排，先煎皮的一邊出油，煎至金黃色，反轉煎約1分鐘後夾起，不用全熟\r\n3. 把雞扒/雞排切成小塊\r\n4. 中火熱鍋加入麻油，把薑和蒜頭炒香\r\n5. 加入雞件，然後加入醬油、米酒及糖，再炒一炒雞件轉小火燉8-10分鐘蓋上蓋子\r\n6. 開蓋轉大火收汁\r\n7. 加入九層塔，炒1-2分鐘即可上碟'),(2,'酸甜涼拌川耳(五辛素)','','備料:\n 川耳(泡發) 220g\n 小黃瓜 1條/180g\n 蒜末 1茶匙\n 大辣椒 1茶匙\n 白芝麻 點綴\n \n 調味:\n 醬油膏 2大匙\n 香油 1大匙\n 白醋 1茶匙\n 砂糖 1茶匙\n 味精 1/4茶匙\n \n 步驟:\n 1. 川耳加熱水浸泡20分鐘\n 2. 川耳洗淨，下鍋焯水2~3分鐘，控乾備用\n 3. 盆中加入蒜末、辣椒圈、醬油膏、香油、白糖、白醋、味精，攪拌均勻\n 4. 小黃瓜切波浪片，所有材料翻拌均勻\n 5. 裝盤，撒上芝麻粒點綴'),(3,'番茄炒蛋','','食材:\r\n蕃茄    2-3個\r\n雞蛋    3顆\r\n糖      1茶匙\r\n蕃茄醬  1湯匙\r\n蔥花    適量\r\n鹽      適量\r\n\r\n步驟:\r\n1. 蔥洗淨切成蔥花\r\n2. 洗淨然後在蕃茄底部輕輕界十字\r\n3. 中火把水煮至沸騰， 加入蕃茄煮約30-45秒即可\r\n4. 把蕃茄加入冷水一會再取出\r\n5. 煮過的蕃茄很容易就能去皮把蕃茄去皮後切塊\r\n6. 把雞蛋打散，加鹽攪拌均勻\r\n7. 中火熱鍋加油和蕃茄，加入蕃茄醬及糖炒至軟身及收汁後備用\r\n8. 中火熱鍋後加油及雞蛋，蛋液邊缘漸漸凝固後把蛋液往中間推\r\n9. 雞蛋5成熟時加入蕃茄關火繼續炒，利用餘溫將蛋液炒熟，加入少許鹽調味，攪拌均勻即可'),(4,'蔥爆豬五花','','食材:\r\n豬五花     500g\r\n蔥         3根\r\n大蒜       3顆\r\n鹽         1小匙\r\n胡椒       1小匙\r\n醬油       2大匙\r\n米酒       1大匙\r\n糖         1小匙\r\n香油       1小匙\r\n\r\n步驟:\r\n1. 豬五花切長條狀， 蔥白蔥綠切小段分開、大蒜切片。 醬油2大匙、糖一小匙、米酒一小匙、香油一小匙\r\n2. 豬五花直接入炒鍋、開中火逼出油。\r\n3. 在逼出的油中煎至金黃色。\r\n4. 瀝乾油的豬五花盛出備用,鍋中放一小匙豬油爆香蔥白、蒜片。\r\n5. 把豬五花倒回鍋中拌炒。\r\n6. 將調料，鹽、胡椒、醬油、糖放入翻炒，米酒沿著鍋邊淋下、香油接著下翻炒拌勻。\r\n7. 最後把蔥綠加入快速翻炒即可裝盤。\r\n8. 焦香的蔥爆豬五花下酒好菜上桌'),(5,'青椒炒肉絲','','食材:\r\n青椒    1 個\r\n蒜頭    少許\r\n豬肉絲  1 盒\r\n醬油    少許\r\n鹽巴    少許\r\n\r\n步驟:\r\n1. 青椒切絲備用、蒜頭切蒜末，肉絲先用少許醬油醃15 -20分鐘\r\n2. 起油鍋爆香蒜頭\r\n3. 先稍微炒一下青椒後起鍋備用\r\n4. 炒肉絲至8分熟時\r\n5. 再加入炒好的青椒\r\n6. 起鍋前一點點鹽巴調味\r\n7. 青椒肉絲完成囉～\r\n\r\n\r\n\r\n\r'),(6,'菠菜番茄炒蛋','https://cookpad.com/tw/%E9%A3%9F%E8%AD%9C/16630778?utm_source=chatgpt.com','用料：菠菜 1 把、番茄 1–2 顆、雞蛋 2 顆、蒜成末少許、油、鹽\n1. 菠菜洗淨切段，番茄切塊，雞蛋打散。\n2. 熱鍋下油，先炒蛋至七八分熟後盛出。\n3. 爆香蒜末，下番茄翻炒至出汁。\n4. 放入菠菜翻炒片刻。\n5. 倒回雞蛋一起炒勻，調味即可。'),(7,'苦瓜炒蛋','https://icook.tw/recipes/423983?utm_source=chatgpt.com','用料：苦瓜 1 條、雞蛋 2–3 顆、鹽、胡椒、油\n1. 苦瓜去籽切薄片，用鹽醃 10 分鐘後沖洗。\n2. 雞蛋打散，加少許鹽、胡椒。\n3. 熱鍋下油，先炒蛋至半熟盛出。\n4. 下苦瓜片快炒，再倒入蛋炒勻即可。'),(8,'青江菜菇菇蒸豆腐','https://m.xiachufang.com/recipe/102214660/?utm_source=chatgpt.com','用料：嫩豆腐 1 塊、青江菜 1 把、香菇/金針菇適量、蒜末、蔥花、醬油、香油\n1. 豆腐切片放盤中，鋪上菇類，青江菜圍邊。\n2. 淋上醬油、香油與少許水的醬汁。\n3. 蒸 8–10 分鐘，取出後撒蔥花即可。'),(9,'紅蘿蔔炒冬粉','https://icook.tw/recipes/463256?utm_source=chatgpt.com','用料：冬粉 1 把、紅蘿蔔絲 1 根、木耳/香菇絲適量、蒜末、蔥段、蛋 1 顆、調味料（醬油、胡椒、香油）\n1. 冬粉泡軟備用。\n2. 蛋炒至半熟盛出。\n3. 爆香蒜末，下紅蘿蔔與木耳快炒。\n4. 加入冬粉與蛋同炒，調味即可。'),(10,'茄子彩椒肉末煲','https://m.xiachufang.com/recipe/107555260/?utm_source=chatgpt.com','用料：茄子 1 條、彩椒 1 顆、絞肉 150g、蒜末、薑片、調味料（醬油、生抽、糖、蠔油、水）\n1. 茄子切條泡鹽水防變黑；彩椒切丁。\n2. 熱鍋爆香蒜末與薑片，下絞肉炒至變色。\n3. 加入茄子炒軟，再放彩椒拌炒。\n4. 倒入調味料，小火煮至茄子軟透、收汁即可。'),(11,'涼拌小黃瓜','https://icook.tw/recipes/384782','用料：小黃瓜 2 條（約 300 g）、蒜末 1 小匙（約 5 g）、白醋 2 大匙（30 m...'),(12,'蕃茄炒青江菜','https://icook.tw/recipes/481282','用料：蕃茄 2 顆（約 300 g，滾刀塊）、青江菜 1 把（約 250 g，葉梗分切 4–5...'),(13,'蒜香炒空心菜','https://icook.tw/recipes/225947','用料：空心菜 1 把（約 300 g，葉梗分段 6–7 cm）、蒜頭 3 瓣（2 瓣切片＋1 ...'),(14,'玉米濃湯','https://icook.tw/recipes/276965','用料：玉米粒 1 罐（約 300 g，保留 1/3 粒狀備用）、鮮奶 200 ml、洋蔥 半顆...'),(15,'馬鈴薯煎餅','https://icook.tw/recipes/419035','用料：馬鈴薯 2 顆（約 400 g，去皮粗洞擦絲）、雞蛋 1 顆（約 50 g）、中筋麵粉 ...'),(21,'家常炒南瓜','https://icook.tw/recipes/443724','用料：南瓜 400 克、蒜頭 3 瓣、食用油 1.5 大匙、鹽 1/3 小匙\n1. 南瓜去皮去籽切薄片（約 0.5 公分厚），蒜頭切片。\n2. 鍋中加 1.5 大匙油，中火爆香蒜片 20 秒。\n3. 放入南瓜片，翻炒 3 分鐘至邊緣略透明。\n4. 加入鹽 1/3 小匙，續炒 2 分鐘至南瓜軟化。判斷依據：筷子能輕鬆插入即熟。'),(22,'洋蔥炒蛋','https://icook.tw/recipes/23674','用料：洋蔥 半顆（約 120 克）、雞蛋 3 顆、食用油 1 大匙、鹽 1/3 小匙\n1. 洋蔥去皮切絲；雞蛋打散加鹽調勻。\n2. 鍋中加油 1 大匙，中火將蛋液炒至七分熟盛出。\n3. 同鍋下洋蔥絲，大火翻炒 2 分鐘至透明。\n4. 倒回雞蛋翻炒 1 分鐘混勻。判斷依據：洋蔥軟透帶甜、蛋熟透不焦。'),(23,'薑絲炒大白菜','https://icook.tw/recipes/215480','用料：大白菜 半顆（約 500 克）、薑絲 20 克、食用油 1.5 大匙、鹽 1/3 小匙\n1. 大白菜洗淨切塊，葉與梗分開；薑去皮切絲。\n2. 鍋中加油 1.5 大匙，中火爆香薑絲 20 秒。\n3. 下白菜梗炒 2 分鐘至半透明，再加葉子大火翻炒 2 分鐘。\n4. 加鹽 1/3 小匙調味，翻炒 30 秒。判斷依據：白菜葉鮮綠、梗脆嫩。'),(24,'香煎杏鮑菇','https://icook.tw/recipes/235104','用料：杏鮑菇 300 克、食用油 1.5 大匙、鹽 1/3 小匙、黑胡椒粉 1/4 小匙\n1. 杏鮑菇洗淨後切厚片（約 1 公分）。\n2. 平底鍋加油 1.5 大匙，放入杏鮑菇片，中火每面煎 2 分鐘至金黃。\n3. 撒鹽與黑胡椒調味，再翻面煎 1 分鐘。\n4. 判斷依據：杏鮑菇外表金黃、內部多汁。'),(37,'清炒大白菜','https://icook.tw/recipes/39792','用料：大白菜 半顆（約 500 克）、蒜頭 3 瓣、食用油 1.5 大匙、鹽 1/3 小匙\n0. 大白菜洗淨後將梗與葉分開，梗切成 4 公分段，葉切大片；蒜頭去皮切末。\n1. 大火熱鍋 1 分鐘，下油 1.5 大匙，放入蒜末爆香約 15 秒。\n2. 下白菜梗，大火快炒 1 分鐘至半透明。\n3. 下白菜葉，續炒 1 分鐘至葉子軟化、顏色翠綠。\n4. 加鹽 1/3 小匙，翻炒均勻，立刻起鍋保持脆嫩。'),(38,'韭菜炒蛋','https://icook.tw/recipes/12954','用料：韭菜 200 克、雞蛋 3 顆、鹽 1/4 小匙、食用油 1 大匙\n0. 韭菜洗淨，切成 3–4 公分段；雞蛋打入碗中加鹽打散。\n1. 熱鍋 1 分鐘，下油 1 大匙，倒入蛋液，中火快速攪動，炒至七分熟後盛出。\n2. 同鍋加少許油，轉大火，放入韭菜翻炒 40 秒至鮮綠。\n3. 倒回雞蛋，快速翻炒 30 秒至全熟，立即起鍋。'),(39,'白蘿蔔排骨湯','https://icook.tw/recipes/37044','用料：白蘿蔔 500 克、豬肋排 600 克、薑片 4 片、蒜頭 3 瓣、水 1500 毫升、鹽 1 小匙\n0. 白蘿蔔去皮切厚塊；豬肋排切段後放入冷水鍋煮滾 3 分鐘去血水，撈出沖洗乾淨。\n1. 湯鍋中加水 1500 毫升，下排骨、薑片、拍碎蒜頭，大火煮滾後轉小火。\n2. 加入白蘿蔔塊，小火燉 40 分鐘，撇去浮沫。\n3. 加鹽 1 小匙調味，再煮 5 分鐘即可。'),(40,'三杯杏鮑菇','https://icook.tw/recipes/255664','用料：杏鮑菇 400 克、薑片 6 片、蒜頭 5 瓣、醬油 2 大匙、米酒 2 大匙、砂糖 1 小匙、麻油 2 大匙\n0. 杏鮑菇洗淨切厚片；薑切片；蒜頭去皮拍碎。\n1. 熱鍋下麻油 2 大匙，中火爆香薑片與蒜頭 1 分鐘。\n2. 放入杏鮑菇片，中火煎至雙面金黃（約 3 分鐘）。\n3. 倒入米酒 2 大匙 + 醬油 2 大匙 + 砂糖 1 小匙，翻炒均勻。\n4. 小火燜煮 3 分鐘至湯汁收乾，鍋中略帶焦香即可起鍋。'),(47,'蒜香炒四季豆','https://icook.tw/recipes/227454','用料：四季豆 300 克、蒜頭 3 瓣、食用油 1.5 大匙、鹽 1/3 小匙\n1. 四季豆洗淨後摘去頭尾並去除粗筋，切段約 5 公分。\n2. 燒一鍋水，加入 1 小匙鹽和幾滴油，將四季豆汆燙約 2 分鐘撈出瀝乾。\n3. 鍋中加 1.5 大匙油，爆香蒜末 15 秒，下四季豆大火快炒 2–3 分鐘。\n4. 加鹽 1/3 小匙調味，翻炒均勻即可起鍋。'),(48,'洋蔥炒雞腿肉','https://icook.tw/recipes/189250','用料：去骨雞腿肉 300 克、洋蔥 半顆（約 120 克）、蒜頭 2 瓣、醬油 1.5 大匙、食用油 1 大匙\n1. 去骨雞腿肉切塊，用 1 大匙醬油醃 10 分鐘。\n2. 洋蔥去皮切絲；蒜頭切末。\n3. 鍋中加 1 大匙油，爆香蒜末 15 秒，下雞腿肉大火翻炒至表面變色。\n4. 加入洋蔥絲，持續翻炒 2 分鐘至軟化出香氣。\n5. 補 0.5 大匙醬油，快速翻炒均勻至雞腿肉熟透即可。'),(49,'地瓜葉蒜蓉炒','https://icook.tw/recipes/23444','用料：地瓜葉 300 克、蒜頭 4 瓣、食用油 1.5 大匙、鹽 1/3 小匙\n1. 地瓜葉摘去粗梗，僅留嫩葉與細梗，洗淨瀝乾。\n2. 蒜頭去皮切末。\n3. 鍋中加 1.5 大匙油，放入蒜末大火爆香 15 秒。\n4. 放入地瓜葉，大火快速翻炒 1–2 分鐘至葉片軟化、仍保持翠綠。\n5. 加鹽 1/3 小匙調味，翻炒均勻即可起鍋。'),(50,'冬瓜排骨湯','https://icook.tw/recipes/22939','用料：冬瓜 500 克、排骨 500 克、薑片 4 片、蒜頭 3 瓣、水 1500 毫升、鹽 1 小匙\n1. 排骨切段，冷水下鍋汆燙 3 分鐘去血水，撈出沖洗乾淨。\n2. 冬瓜去皮去籽切成厚塊；薑切片；蒜頭拍碎。\n3. 湯鍋加水 1500 毫升，放入排骨、薑片和蒜頭，大火煮滾後轉小火燉 30 分鐘。\n4. 加入冬瓜，小火再煮 20 分鐘至透明軟爛。\n5. 加鹽 1 小匙調味，繼續煮 5 分鐘即可。'),(51,'椒鹽茄子','https://icook.tw/recipes/22267','用料：茄子 2 條（約 400 克）、蒜頭 3 瓣、食用油 2 大匙、鹽 1/3 小匙、胡椒粉 1/4 小匙\n1. 茄子洗淨後切長條，泡鹽水 10 分鐘後撈起擦乾。\n2. 蒜頭切末。\n3. 平底鍋加 2 大匙油，放入茄子中火煎至雙面金黃，盛出備用。\n4. 鍋內留少許油，下蒜末炒香 10 秒，放回茄子翻炒。\n5. 撒鹽 1/3 小匙與胡椒粉 1/4 小匙，翻炒均勻即可起鍋。');
/*!40000 ALTER TABLE `recipes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (8,'rex','a0916996002@gmail.com','$2b$12$c41zvIEzm7BoyZQxlxt/i.Wyi28jFSqGKgI8.DE8d31P/ZlslniVW'),(9,'真．爆炸王','huang@gmail.com','$2b$12$KyvUuCNs.OGrf01IKwel4.1gBfDbO6pgeCel9R5l9R.0D4zAyBd5S'),(11,'小小放電Lovely','Lorelody@mail.com','$2b$12$iS1U9n0LGKTgMFHt.EKbTOwjZaSgXrfsluD1yrWAIQ.GbeCcd0GZW'),(12,'超級無敵律師','Phloryana@mail.com','$2b$12$r4ldwjSbcbqiRu8PNqdqI.JNlkoswoyuPX24qEzFmO3uCmOx1AHEK'),(13,'軟綿綿黃金少女','Zirgruzath@mail.com','$2b$12$O0F5DNbLmHv6Rs3206P.7euK9MoAlhs59MbYnJdD6G1TBgAsSFXOK'),(14,'軟綿綿洗廁所劍士','Pireete@mail.com','$2b$12$UBGGKrVLSbxrZJAQ/zR9geUn5XI63JUQmH/JoqOesYKfApEKn6PNi'),(15,'英明威武懶惰巫女','Conwirua@mail.com','$2b$12$3dT3Llk6EEY3Sfnmy1/tOewe0oh.WdQQ8ZiMSaWdk4/jVI8WgT1CG'),(16,'超科學放電的右腕','Landithor@mail.com','$2b$12$LmK9g/rlDYmB50G1QWkUaevSy/COoMOD2vmNrmMym7oC9vzecHMuS'),(17,'科學的拼裝少年','Briqir@mail.com','$2b$12$6h8S9Co0102l6mjYy1Ppu.NIXoQnbFyyDtuneTPpvpExbVdycFDYS'),(18,'細肩帶大總統','Phonnorus@mail.com','$2b$12$7c1FSvnp5fdUdZawDMdvv.wGtxJF.58iLkUFpDm8ZGmjt4x4/6a52'),(19,'超能花樣少女','Jizyal@mail.com','$2b$12$b5fZaJQ6w67ART6b5QuH4.ROkxGbBKfNfpfqfS0tTq5yGqv/dGarm');
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

-- Dump completed on 2025-11-24  6:02:55
