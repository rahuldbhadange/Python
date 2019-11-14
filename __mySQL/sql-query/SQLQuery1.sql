



USE mytestdb
select * FROM mytest



-- UPDATE PRIMARY KEY
-- ALTER TABLE PROFILE_3 ADD PRIMARY KEY (ID);




------- ALTER TABLE -------
ALTER TABLE Persons ADD PRIMARY KEY (ID);

SELECT * FROM PROFILE_3;
SELECT * FROM PROFILE_4;

ALTER TABLE PROFILE_3
ADD FOREIGN KEY (ID) REFERENCES PROFILE_4(ID);

SELECT * FROM PROFILE_3;
SELECT * FROM PROFILE_4;



---- COMPARING RECORDS BETn TWO DIFFt TABLES ---
SELECT * FROM PROFILE_3;
SELECT * FROM PROFILE_4;

SELECT PROFILE_4.FNAME, PROFILE_4.SALARY 
FROM PROFILE_3, PROFILE_4 
WHERE PROFILE_3.ADDR = PROFILE_4.ADDR




------------------------------------------------------ HAVING (COUNT, AS, GROUP BY, DESC) ------------------------------------------------------------------
USE mytestdb
SELECT * FROM PROFILE_1;
SELECT * FROM PROFILE_2;
SELECT * FROM PROFILE_3;
SELECT * FROM PROFILE_4;

SELECT ADDR, SALARY FROM PROFILE_4;
SELECT ADDR, COUNT(SALARY) FROM PROFILE_4 GROUP BY ADDR HAVING COUNT(SALARY) > 1 ORDER BY COUNT(SALARY);
SELECT ADDR FROM PROFILE_4 GROUP BY ADDR HAVING COUNT(SALARY) > 1 ORDER BY COUNT(SALARY);
SELECT ADDR, COUNT(SALARY) AS 'COUNT' FROM PROFILE_4 GROUP BY ADDR HAVING COUNT(SALARY) > 0 ORDER BY COUNT(SALARY);
SELECT ADDR, COUNT(SALARY) AS 'COUNT' FROM PROFILE_4 GROUP BY ADDR HAVING COUNT(SALARY) > 0 ORDER BY COUNT(SALARY) DESC;


SELECT * FROM PROFILE_4
WITH CTE AS (
SELECT ADDR, COUNT(SALARY)
 