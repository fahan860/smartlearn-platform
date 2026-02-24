# MySQL Database Setup for Smart Learning Platform

This document describes the setup of the MySQL database used in the Smart Learning Platform,
including schema creation, seeding data, common issues, solutions, and verification steps.

---

## 1. Database Overview

The MySQL database stores **structured and transactional data**:

- `users`: registered users of the platform  
- `courses`: available courses  
- `enrollments`: which users are enrolled in which courses  

Other data (e.g., user interactions) is stored in MongoDB for flexibility.

---

## 2. Creating the Database

The MySQL container is launched using Docker:

```powershell
docker run --name smartlearn-mysql `
  -e MYSQL_ROOT_PASSWORD=root `
  -e MYSQL_DATABASE=smart_learning `
  -e MYSQL_USER=smartuser `
  -e MYSQL_PASSWORD=smartpass `
  -p 3307:3306 `
  -d mysql:8.0


Notes:

Host port 3307 avoids conflicts with local MySQL.

Root password: root

Backend user: smartuser, password: smartpass

## 3. Applying the Schema (schema.sql)
Problem Encountered

Using PowerShell redirection < failed:

L’opérateur « < » est réservé à une utilisation future


Using smartuser initially gave an access denied error:

Access denied for user 'smartuser'@'localhost'

Solution

Connect as root for initial import.

Copy the schema file into the container to avoid PowerShell redirection issues:

docker cp database\mysql\schema.sql smartlearn-mysql:/schema.sql
docker exec -it smartlearn-mysql bash
mysql -u root -p smart_learning < /schema.sql


Using root avoids access issues caused by user host restrictions (smartuser@'%' vs smartuser@'localhost').

## 4. Applying Seed Data (seed.sql)

Populate tables with test data:

docker cp database\mysql/seed.sql smartlearn-mysql:/seed.sql
docker exec -it smartlearn-mysql bash
mysql -u root -p smart_learning < /seed.sql


Seed data includes users, courses, and enrollments.

Required for testing recommendation algorithms and Spark processing.

## 5. Verification
Option 1: MySQL interactive
mysql -u root -p
USE smart_learning;
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM courses;
SELECT * FROM enrollments;

Option 2: Command line
mysql -u root -p -e "USE smart_learning; SHOW TABLES;"
mysql -u root -p -e "USE smart_learning; SELECT * FROM users;"


Expected tables:

users

courses

enrollments

Seeded data should be present for testing.