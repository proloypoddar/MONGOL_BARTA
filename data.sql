CREATE DATABASE membership_db;

USE membership_db;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    membership ENUM('free', 'premium') DEFAULT 'free'
);
