-- MySql database for the blog designed by yanshuzh

-- To reload the tables:
--   mysql --user=blog --password=blog --database=blog < schema.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    markdown MEDIUMTEXT NOT NULL,
    html MEDIUMTEXT NOT NULL,
    published DATETIME NOT NULL,
    classifyid int NOT NULL,
    classifyname VARCHAR(20),NOT NULL,
    KEY (published)
);

DROP TABLE IF EXISTS authors;
CREATE TABLE authors (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    passwd VARCHAR(100) NOT NULL,
    aboutme MEDIUMTEXT NOT NULL,
    record int NOT NULL,
    moodrecord int Not NULL
);

DROP TABLE IF EXISTS classify;
CREATE TABLE classify (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    classifyid int NOT NULL,
    classifyname VARCHAR(20),NOT NULL
);
