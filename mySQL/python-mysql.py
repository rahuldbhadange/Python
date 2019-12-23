# Python MySQL

# Python can be used in database applications. One of the most popular databases is MySQL.

# Python needs a MySQL driver to access the MySQL database.

# Python needs a MySQL driver to access the MySQL database.

# In this tutorial we will use the driver "MySQL Connector".

# We recommend that you use PIP to install "MySQL Connector".

# PIP is most likely already installed in your Python environment.

# C:\Users\Your Name\AppData\Local\Programs\Python\Python36-32\Scripts>python -m pip install mysql-connector
#         why we use -m ?


# mysql.connector == pymysql

import mysql.connector
import pymysql


mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword"
)



print(mydb)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)


pymydb = pymysql.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword"
)


mycur = pymydb.cursor()

mycur.execute()