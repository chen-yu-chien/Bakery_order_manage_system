-- --------------------------------------------------------
-- 主機:                           
-- 伺服器版本:                        8.0.36 - MySQL Community Server - GPL
-- 伺服器作業系統:                      Win64
-- HeidiSQL 版本:                  12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 傾印 bakery 的資料庫結構
CREATE DATABASE IF NOT EXISTS `bakery` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bakery`;

-- 傾印  資料表 bakery.breads 結構
CREATE TABLE IF NOT EXISTS `breads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `stock` int NOT NULL,
  `imgUrl` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '圖片的minIO url',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在傾印表格  bakery.breads 的資料：~6 rows (近似值)
DELETE FROM `breads`;
INSERT INTO `breads` (`id`, `name`, `price`, `description`, `stock`, `imgUrl`) VALUES
	(1, '法式麵包', 50, '經典的法式麵包，酥脆香氣撲鼻。', 10, NULL),
	(2, '義大利麵包', 60, '軟滑的義大利麵包，入口即化。', 8, NULL),
	(3, '芝士麵包', 70, '濃郁的芝士風味，讓人無法抗拒。', 5, NULL),
	(4, '巧克力麵包', 80, '香甜的巧克力麵包，濃情蜜意。', 12, NULL),
	(5, '草莓麵包', 75, '新鮮草莓風味，甜而不膩。', 7, NULL),
	(6, '堅果麵包', 90, '含有豐富的堅果，香氣十足。', 3, NULL);

-- 傾印  資料表 bakery.customers 結構
CREATE TABLE IF NOT EXISTS `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在傾印表格  bakery.customers 的資料：~10 rows (近似值)
DELETE FROM `customers`;
INSERT INTO `customers` (`id`, `name`, `telephone`, `address`) VALUES
	(1, '王小明', '0987654321', '台北市中正區信義路100號'),
	(2, '陳美麗', '0912345678', '台中市西屯區文心路200號'),
	(3, '李國華', '0932123456', '高雄市左營區博愛路300號'),
	(4, '林雅雯', '0922334455', '新北市板橋區中山路400號'),
	(5, '張志強', '0966332211', '桃園市中壢區中正路500號'),
	(6, '黃志強', '0911234567', '台北市大安區和平東路1段50號'),
	(7, '王麗珍', '0922444666', '台中市南區建國路2段150號'),
	(8, '劉浩然', '0933555777', '高雄市三民區建國路3段250號'),
	(9, '陳建宏', '0944888999', '新北市三重區中興路500號'),
	(10, '許晴雯', '0955990000', '台南市北區府前路1段600號');

-- 傾印  資料表 bakery.orders 結構
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customerid` int NOT NULL,
  `orderdate` date NOT NULL,
  `breadid` int NOT NULL,
  `quantity` int NOT NULL,
  `pickup` int NOT NULL COMMENT '-1: 已取貨，0: 自取，1: 宅配',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在傾印表格  bakery.orders 的資料：~15 rows (近似值)
DELETE FROM `orders`;
INSERT INTO `orders` (`id`, `customerid`, `orderdate`, `breadid`, `quantity`, `pickup`) VALUES
	(1, 1, '2024-11-06', 1, 2, -1),
	(2, 2, '2024-11-14', 2, 3, 0),
	(3, 3, '2024-11-10', 3, 1, -1),
	(4, 4, '2024-11-12', 4, 4, 1),
	(5, 5, '2024-11-09', 5, 5, 0),
	(6, 1, '2024-11-01', 1, 2, 1),
	(7, 2, '2024-11-02', 2, 3, 0),
	(8, 3, '2024-11-03', 3, 1, -1),
	(9, 4, '2024-11-04', 4, 4, 1),
	(10, 5, '2024-11-05', 5, 5, 0),
	(11, 6, '2024-11-06', 6, 2, 1),
	(12, 7, '2024-11-07', 1, 3, 0),
	(13, 8, '2024-11-08', 5, 1, -1),
	(14, 9, '2024-11-09', 3, 4, 1),
	(15, 10, '2024-11-10', 4, 5, 0);

-- 傾印  資料表 bakery.staffs 結構
CREATE TABLE IF NOT EXISTS `staffs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在傾印表格  bakery.staffs 的資料：~5 rows (近似值)
DELETE FROM `staffs`;
INSERT INTO `staffs` (`id`, `username`, `password`) VALUES
	(1, 'johndoe', '123456'),
	(2, 'janesmith', 'abcdef'),
	(3, 'michaelchan', 'password'),
	(4, 'lindawong', 'qwerty'),
	(5, 'alexlee', 'letmein');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
