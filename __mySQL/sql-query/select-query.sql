-- ALL SCENARIO OF SELECT QUERY --



------- DISTINCT RETURNS ONLY Unique Record FROM TABLE
select DISTINCT rollno, firstname from mytesttable



------------------------------------------------- BETWEEN \ AND-------------------------------------------------
select rollno, firstname, lastname from mytesttable where rollno BETWEEN 1 and 3

use mytestdb
select rollno, firstname, lastname from mytesttable where rollno between 2 and 6 -- WILL RETURNS WHER ROLLNO = 2 TO 6 (INCLUDES BOTH)


------------------------------------------------- IN -------------------------------------------------
use mytestdb
select rollno, firstname, lastname from mytesttable where rollno IN (2, 6) -- WILL ONLY RETURNS WHER ROLLNO = 2 AND 6



------------------------------------------------- NOT IN -------------------------------------------------
use mytestdb
select rollno, firstname, lastname from mytesttable where rollno NOT IN (2, 6) -- WILL ONLY RETURNS WHER ROLLNO <> 2 and 6




--------------------------- OPERATOR (AND, OR, LIKE[%], <, >, <> , = ,)----------------------------------
use mytestdb

select rollno, firstname from mytesttable

select firstname, rollno from mytesttable where lastname = 'zari'

select firstname, rollno from mytesttable where lastname like '%ge'

select firstname, rollno from mytesttable where lastname like '%ge'

select rollno, firstname from mytesttable where rollno <> 2

select rollno, firstname, lastname from mytesttable where rollno like '%411'

select rollno, firstname from mytesttable

select firstname, rollno from mytesttable where lastname = 'zari'

select firstname, rollno from mytesttable where lastname like '%ge'

select firstname, rollno from mytesttable where lastname like '%ge'

select rollno, firstname from mytesttable where rollno <> 2

select rollno, firstname, lastname from mytesttable where rollno like '%411'

select rollno, firstname, lastname from mytesttable where rollno < '6' 

select rollno, firstname, lastname from mytesttable where rollno < 6 and rollno > 2 ---- GREATER THAN \ LESS THAN

select rollno, firstname, lastname from mytesttable where firstname like '%h%'

select rollno, firstname, lastname from mytesttable where rollno like '%411' and firstname <> 'Rahul'

select rollno, firstname, lastname from mytesttable where rollno <> 2 and firstname <> 'Rahul' ---- NOT EQUAL TO

select rollno, firstname, lastname from mytesttable where rollno <> 2 OR firstname <> 'rahul'




------------------- CRATING NEW COLUMN\TABLE OUT OF QUERY STATEMENT (AS, INTO, FROM) ----------

select rollno, firstname, lastname, rollno * 10 as salary from mytesttable -- CRATING NEW COLUMN\TABLE


select rollno, firstname, lastname, rollno * 10 as salary into mytesttable_11 from mytesttable -- CRATING NEW COLUMN INTO NEW TABLE

select rollno, firstname, lastname, salary, (salary + salary * 100) as 'revised_salary' into mytesttable_44 from mytesttable_11

select firstname, lastname, rollno * 10 as salary into mytesttable_22 from mytesttable

select firstname, lastname, rollno * 10 as salary into mytest from mytesttable
