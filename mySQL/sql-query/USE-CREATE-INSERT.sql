---------------------------------------------------- CRATE DATABASE ----------------------------------------------------
create database mytestdb
CREATE DATABASE MYDB



---------------------------------------------------- CREATE TABLE - WITHOUT PRIMARY KEY ----------------------------------------------------
use mytestdb
create table mytesttable (rollno int NOT NULL , firstname varchar(50), lastname varchar(50))




---------------------------------------------------- CREATE TABLE - WITH PRIMARY KEY & IDENTITY (AUTO_INCREMENT) ----------------------------------------------------
USE mytestdb
CREATE TABLE PROFILE_4 (ID INT NOT NULL IDENTITY(1,1) PRIMARY KEY, AGE INT, FNAME VARCHAR(250), LNAME VARCHAR(250), ADDR VARCHAR(150), SALARY FLOAT);



---------------------------------------------------- CREATE TABLE - WITH PRIMARY KEY ----------------------------------------------------
USE mytestdb;
CREATE TABLE PROFILE_1 (ID INT NOT NULL, AGE INT, FNAME VARCHAR(150), LNAME VARCHAR(150), ADDR VARCHAR(1555), SALARY FLOAT, PRIMARY KEY (ID));
INSERT INTO PROFILE_1 VALUES (1, 20, 'RAHUL', 'BHADANGE', 'NASHIK', 49599.56);
SELECT * FROM PROFILE_1;


USE mytestdb
CREATE TABLE PROFILE_2 (ID INT NOT NULL PRIMARY KEY, AGE INT, FNAME VARCHAR(250), LNAME VARCHAR(250), ADDR VARCHAR(150), SALARY FLOAT);
INSERT INTO PROFILE_2 VALUES (1, 20, 'RAHUL', 'BHADANGE', 'NASHIK', 49599.56);
SELECT * FROM PROFILE_2;


USE mytestdb
CREATE TABLE PROFILE_3 (ID INT NOT NULL, AGE INT, FNAME VARCHAR(250), LNAME VARCHAR(250), 
ADDR VARCHAR(150), SALARY FLOAT)
INSERT INTO PROFILE_3 VALUES (1, 20, 'RAHUL', 'BHADANGE', 'NASHIK', 49599.56);
INSERT INTO PROFILE_3 VALUES (4, 25, 'SAMESH', 'KLJDJBH', 'NASCDHIK', 49599.56);
INSERT INTO PROFILE_3 VALUES (5, 23, 'KRAJESH', 'JDFHSDD', 'FGSNASHIK', 49599.56);
INSERT INTO PROFILE_3 VALUES (6, 23, 'HRAKESH', 'DJKHFSDLNGEKD', 'NASHIKGDF', 49599.56);
SELECT * FROM PROFILE_3;




---------------------------------------------------- INSERT Data ----------------------------------------------------

INSERT INTO mytesttable (rollno, firstname, lastname) values(1, 'rahul', 'bhadange');

insert into mytesttable(rollno, firstname, lastname) values(2, 'kuldip', 'jagtap')

insert into mytesttable(rollno, firstname, lastname) values (3, 'rizwan', 'zari')

insert into mytesttable(rollno, firstname, lastname) values (44444411, 'arun', 'kumar')




---------------------------------------------------- DELETE Records ----------------------------------------------------
USE mytestdb
DELETE from mytesttable_22 where firstname like 'arun'
DELETE from mytesttable_22 where firstname like '%a%'


USE mytestdb
DELETE from PROFILE_4 where FNAME = 'RAJU';
DELETE FROM PROFILE_4 WHERE FNAME LIKE 'SANJU';
DELETE from PROFILE_4 where FNAME like '%H%';
SELECT * FROM PROFILE_4;




------------------------------------------ UPDATE [SET, AS, LIKE, ] ----------------------------------------------------
update mytesttable_22 set firstname = 'Rizwan' where firstname like '%wan' 
-- update mytesttable SET rollno * 10 AS SALARY
-- UPDATE mytesttable SET phone = 95895 where firstname = 'Rahul'


----- MODIFY EXISTING RECORD ----
update mytesttable set firstname = 'Rahul' where lastname like '%ge'

update mytesttable set rollno = 4 where rollno like '%11'