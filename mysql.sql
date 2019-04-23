DROP database if EXISTS mobile_canteen;
create database mobile_canteen character set utf8mb4 collate utf8mb4_unicode_520_ci;
use mobile_canteen;

DROP TABLE if EXISTS customer;
CREATE TABLE customer (
customer_id VARCHAR(64) NOT NULL,
name VARCHAR(64) NOT NULL,
email VARCHAR(64) NOT NULL,
password VARCHAR(64) NOT NULL,
phone VARCHAR(64) NOT NULL
PRIMARY KEY (customer_id));

DROP TABLE if EXISTS vendor;
CREATE TABLE vendor (
vendor_id VARCHAR(64) NOT NULL,
name VARCHAR(64) NOT NULL,
email VARCHAR(64) NOT NULL,
password VARCHAR(64) NOT NULL,
phone VARCHAR(64) NOT NULL,
description TEXT
PRIMARY KEY (vendor_id));

DROP TABLE if EXISTS menu;
CREATE TABLE menu (
dish_id VARCHAR(64) NOT NULL,
vendor_id VARCHAR(64) NOT NULL,
date DATE NOT NULL,
name VARCHAR(64) NOT NULL,
description TEXT,
amount INTEGER NOT NULL,
amount_left INTEGER NOT NULL
PRIMARY KEY (dish_id));

DROP TABLE if EXISTS status;
CREATE TABLE status (
vendor_id VARCHAR(64) NOT NULL,
status VARCHAR(16) NOT NULL,
location VARCHAR(256) NOT NULL
PRIMARY KEY (vendor_id));