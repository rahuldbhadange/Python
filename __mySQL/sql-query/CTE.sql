USE mytestdb
CREATE TABLE TEST_CTE (a int, b int)

INSERT INTO TEST_CTE(a, b) 
VALUES
    (1,1),
    (1,2),
    (1,3),
    (2,1),
    (1,2),
    (1,3),
    (2,1),
    (2,2);

SELECT * FROM TEST_CTE




SELECT a, b, count(*) AS 'OCC' from TEST_CTE GROUP BY a, b
SELECT a, b, count(a) AS 'OCC' from TEST_CTE GROUP BY a, b


SELECT a,b, count(*) AS 'OCC' from TEST_CTE GROUP BY a,b HAVING COUNT(*)>1 


SELECT * FROM TEST_CTE
SELECT a, b, count(*) AS 'OCC' from TEST_CTE GROUP BY a, b
SELECT a,b, count(a) AS 'OCC' from TEST_CTE GROUP BY a,b HAVING COUNT(b)>1 
SELECT a, b, count(b) AS 'OCC' from TEST_CTE GROUP BY a, b HAVING COUNT(a)>1 

--- finding duplicate in multiple row ----
SELECT * FROM TEST_CTE;
with cte as (select a, b, count(*) as 'occ' from TEST_CTE group by a, b 
having count(*)>1) select TEST_CTE.a, TEST_CTE.b 
from TEST_CTE inner join cte on cte.a = TEST_CTE.a and cte.b = TEST_CTE.b 
order by TEST_CTE.a, TEST_CTE.b;


SELECT * FROM TEST_CTE;
with cte as (select a, b, count(*) as 'occ' from TEST_CTE group by a, b 
having count(*)>1) select TEST_CTE.a, TEST_CTE.b 
from TEST_CTE inner join cte on cte.a = TEST_CTE.a and cte.b = TEST_CTE.b 
order by TEST_CTE.b;


USE mytestdb
SELECT * FROM TEST_CTE;
with cte as (select a, b, count(*) as 'occ' from TEST_CTE group by a, b 
having count(*)>1) select TEST_CTE.a, TEST_CTE.b 
from TEST_CTE inner join cte on cte.a = TEST_CTE.a and cte.b = TEST_CTE.b;

--- finding duplicate in single row ----
SELECT * FROM TEST_CTE;

SELECT a, count(a) AS 'OCC' from TEST_CTE GROUP BY a HAVING COUNT(a)>1 
SELECT b, count(b) AS 'OCC' from TEST_CTE GROUP BY b HAVING COUNT(b)>1 

SELECT a,b, count(a) AS 'OCC' from TEST_CTE GROUP BY a,b HAVING COUNT(a)>1 
SELECT a, b, count(b) AS 'OCC' from TEST_CTE GROUP BY a, b HAVING COUNT(b)>1



