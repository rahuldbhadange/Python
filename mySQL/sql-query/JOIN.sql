-- EQUI JOIN - RETURNS ROWS THAT HAVE EQUIVALENT VALUES FOR THE SPECIFIED COLUMN

SELF JOIN
NATURAL JOIN -

INNER JOIN
LEFT OUTER JOIN 
RIGHT OUTER JOIN
FULL JOIN OR FULL OUTER JOIN
CROSS JOIN OR CARTESIAN





USE mytestdb
select * from mytest
select * from mytesttable
select * from mytesttable_11
select * from mytesttable_22

USE mytestdb
select * from mytesttable_222
select * from mytesttable_33
select * from mytesttable_44



----------------------------- INNER JOIN -------------------------------------------------
use mytestdb2
create table pd (id int, firstname varchar(50), lastname varchar(20))

insert into pd values (1, 'ramesh', 'jadhav')
insert into pd values (2, 'paresh', 'patil')
insert into pd values (3, 'suresh', 'wankhade')


use mytestdb2;
create table salary (id int, salary float)

insert into salary values (1, 6045)
insert into salary values (2, 9846)
insert into salary values (3, 4625)


use mytestdb2;

select * from pd;
select * from salary;
SELECT A.firstname, A.lastname, B.salary 
FROM pd A INNER JOIN salary B ON A.id = B.id;



use mytestdb2;

select * from pd;
select * from salary;
SELECT pd.firstname, pd.lastname, salary.salary 
FROM pd INNER JOIN salary ON pd.id = salary.id;



------------------------------------------ LEFT JOIN \ LEFT OUTER JOIN -----------------------------------
USE mytestdb
select * from mytesttable_222
select * from mytesttable_44

USE mytestdb
SELECT A.firstname, A.bonus, 
B.rollno, B.firstname, B.salary, B.revised_salary
FROM mytesttable_222 A LEFT JOIN mytesttable_44 B 
ON A.firstname = B.firstname



USE mytestdb
select * from mytesttable_44
select * from mytesttable_222

USE mytestdb
SELECT A.rollno, A.firstname, A.lastname, A.salary, 
A.revised_salary, B.bonus
FROM mytesttable_44 A LEFT JOIN  mytesttable_222 B 
ON A.firstname = B.firstname



----------------------------------- RIGHT JOIN \ RIGHT OUTER JOIN ---------------------------------
USE mytestdb
select * from mytesttable_44
select * from mytesttable_222


USE mytestdb
SELECT A.rollno, A.firstname, A.lastname, A.salary, 
A.revised_salary, B.bonus
FROM mytesttable_44 A RIGHT JOIN  mytesttable_222 B 
ON A.firstname = B.firstname



USE mytestdb
select * from mytesttable_222
select * from mytesttable_44

USE mytestdb
SELECT A.firstname, A.lastname, A.bonus, 
B.rollno, B.firstname, B.revised_salary
FROM mytesttable_222 A RIGHT JOIN mytesttable_44 B 
ON A.firstname = B.firstname



USE mytestdb
select * from mytesttable_222
select * from mytesttable_44

USE mytestdb
SELECT A.firstname, A.bonus, 
B.rollno, B.firstname, B.salary, B.revised_salary
FROM mytesttable_222 A RIGHT JOIN mytesttable_44 B 
ON A.firstname = B.firstname



---------------------------------------- FULL JOIN - FULL OUTER JOIN ---------------------------------
USE mytestdb
select * from mytesttable_222
select * from mytesttable_44

USE mytestdb
SELECT A.firstname, A.lastname, A.bonus, 
B.rollno, B.firstname, B.revised_salary
FROM mytesttable_222 A FULL OUTER JOIN mytesttable_44 B 
ON A.firstname = B.firstname


USE mytestdb
SELECT * FROM mytesttable_222 A FULL OUTER JOIN mytesttable_44 B 
ON A.firstname = B.firstname



------------------------------------------------ CROSS JOIN - Cartesian Mul ------------------------------------------
USE mytestdb
select * from mytesttable_222
select * from mytesttable_44


USE mytestdb
--SELECT * FROM mytesttable_222 CROSS JOIN mytesttable_44
SELECT * FROM mytesttable_44
SELECT * FROM mytesttable_222


USE mytestdb
SELECT mytesttable_44.firstname, mytesttable_44.lastname, mytesttable_44.revised_salary, 
mytesttable_222.bonus, mytesttable_222.lastname FROM mytesttable_44 CROSS JOIN mytesttable_222



--------------------- Featching Second Highest salary from the salary column -------------------
use mytestdb;
SELECT * FROM mytesttable_44;
select max(salary) from mytesttable_44 where salary not in (select max(salary) from mytesttable_44);
