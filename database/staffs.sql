-- 建立顧客資料表
CREATE TABLE IF NOT EXISTS staffs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);
-- 插入使用者帳號資料
INSERT INTO `staffs` (username, password) VALUES
('johndoe', '123456'),
('janesmith', 'abcdef'),
('michaelchan', 'password'),
('lindawong', 'qwerty'),
('alexlee', 'letmein');

-- 確認資料插入
SELECT * FROM `staffs`;
