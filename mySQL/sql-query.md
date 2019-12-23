INNER JOIN, into #mytest, into mytest, DELETE, values, insert into, INTO, AS, UPDATE, SET, NULL, ISNULL(column_name, base_value(0 or anything)), SELECT, where, =, >, <, <>, like, '%CA', 'CA%', 'AND', 'OR', 'BETWEEN', IN, NOT IN, map-reduce, 

1. Table 2-Rules
2. Table - Normalization
        First Normal Form
        Second Normal Form
        Third Normal Form
        BCNF

Structural Query Language - Queries

    Select * 
    Select ID,username,email from book
    insert into mytesttable(rollno, firstname, lastname) values(6, 'shubham', 'mandloi')
    select username from book where author='ramesh'
    Select * from book where address like '%CA'
    Select * from book where author > 'T'
    Select username, email from book where author <> 'ramesh'
    select rollno, firstname, lastname from mytesttable where rollno <> 2 and firstname <> 'Rahul'
    Select username, ID, email from book where phone like '%5468664'
    Select username from book where author='suresh' AND address like '%CA'
    Select username from book where author='suresh' OR author='ramesh'
    Select ID, username, address from book where date = 2012 BETWEEN 2013 		???????
    UPDATE book SET address = NULL WHERE ID = 2
    UPDATE book SET discount_price = price - (price * 10\100)
    select rollno, firstname, lastname from mytesttable where rollno in (2, 6)
    select firstname, lastname, rollno * 10 as salary into mytesttable_22 from mytesttable
    select firstname, lastname, rollno * 10 as salary into #mytest from mytesttable
    DELETE from mytesttable_22 where firstname like 'arun'
    SELECT A.firstname, A.lastname, B.salary FROM pd A INNER JOIN salary B ON A.id = B.id

