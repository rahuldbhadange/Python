import MySQLdb

db = MySQLdb.connect("localhost", "root", "1234", "TESTDB")

cursor = db.cursor()
cursor.execute ( """
    CREATE TABLE PERSON 
    ( 
     F_NAME CHAR(20) NOT NULL, 
     L_NAME CHAR(20), 
     AGE INT, 
     GENDER CHAR(4)
    )
 """)
cursor.execute( """
    INSERT INTO PERSON (F_NAME, L_NAME, AGE, GENDER)
    VALUES
        ('Neeraj','Lad','22','Male'),
        ('Vivek','Pal','24','Male')  
 """)
print (cursor.rowcount)
