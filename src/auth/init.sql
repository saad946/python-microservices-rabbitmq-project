show databases;

CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'admin321';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255) UNIQUE NOT NULL,password VARCHAR(255) NOT NULL);

INSERT INTO user (username,password) VALUES ('saadullah946@gmail.com', 'admin321');

show tables;

describe user;

select * from user;