OOPS:Object-Oriented Programming Structure

Features of OOPS

1.Encapsulation
2.Abstraction
3.Inheritence
4.polymorphism


The above OOPS principles provides
security,
flexibility and
re-usability.


ex:secutity: Bank Application--->Bank consisting of 'n' no of
 customers,one customer details cannot be viewed by another
 customer,this application is providing security.
 
 flexibility:for deposit operation, we have got flexibility for
 depositing in many ways such as manual,through cheques,DD's etc
 

 re-usability:ATM application is developed once but can be
 reused for many times.

 Even python supports OOPS,so the python applications will also
 achieve all the above features.
 
 In java,the developer is forced to write programs using oops
 principles only,we cannot develop applications witout OOps
 
 But in python,we can write programs using
 1.Procedural-oriented programming
 2.Object-Oriented programming

------------------------------------------------------------------------------
 1) Encapsulation :-
 Every application has data and operations.
 Data represented using variables
 operations represented using functions/methods
 
 //customer--->data  //all are global variables
 cname="miller"
 caccno=501234678
 caddr="Ameerpet"
 bal=50000

 //customer operations (functions)
def deposit(damt):
    pass
def withdraw(wamt):
    pass
def transfer(daccno,tamt):
     pass
Note:damt,wamt,daccno,tamt are the local variables to the respective function
cname,caccno,caddr,bal are global variables which can be accessed by all the fuctions

damt is a local variable of deposit(),so only deposit() can
access damt, but not by other functions 
so local variables can be executed by only the particular
method

//emp--->data
 ename="James"
 eid=101
 esal=30000
 eaddr="hyd"
//emp operations
def da():
    pass
def hra():
    pass
def pf():
    pass

in the above example, all the global variables of customer and
emp can be accessed by all the fuctions of customer and emp

actually-->customer data should be accessed by customer functions
 and emp data should be accessed by emp functions only but here
customer data is accessed by both customer and emp functions
and similarly emp data is accessed by both customer and emp
functions.
so we need to make customer data available only to customer functions
similarly we need to make the emp data available only to emp functions

so the process of grouping/binding related data along with
methods(functionalities) is called as Encapsulation

Encapsulation: The process of grouping/binding related data
along with methods(functionalities) is called encapsulation.

Encapsulation is implemented by using class
------------------------------------------------------------------------------

Class: A class is a structure which groups/binds the related
data along with methods.
A class is a collection of variables and methods
Data is represented using variables and
operations are represented using methods
In class,we can have 2 types of variables,
1.Static variables
2.Non-static variables

syntax of class :
    class classname:
        """doc string"""
        ----------------
        ----------------
        ---------------- -------->data(variables)+methods
        ----------------
        ----------------

A class consists of the following:
    1.Doc string
    2.Variables
       i. static variable
       ii.Non-static variable
    3.Methods

cname,-----------------
caddr,
caccno
cbal                   --------->customer group,
deposit()                        consisting of data(variables)
transfer()                       such as cname,caddr,caccno,cbal 
withdraw()-------------          deposit(),transfer() and withdraw()
                                 are the methods.

ename------------------
eid
esal
design                ----------->emp group
TA()
DA()
HRA()
PF()-------------------

in the above example,we have got 2 groups,

customer group and emp group, we can represent by 2 classes
in customer group, customer variables can be accesssed only
by customer methods but not by emp methods.
similarly,in emp group, emp variables can be accessed only by
emp methods but not by customer methods.
variables or methods of one class cannot be accessed by another
class.

-----------------------------------------------------------------------------------

Abstraction: Hiding up of data and methods of a  class.
ex: properties of one class cannot be accessed by another
class.
if customer class is given to a bank,then for 'n' no of
customers, only one class is created or used, but 'n' no of
objects are created for the customer class such as c1,c2,c3...




object: An object is an instance of a class
A class is a collection of similar objects.
we can create 'n' no of objects for a class
each object will have its own copy of variables and methods

---------------------------------------------------------------------------

Inheritance: Inheritance is the process of acquiring the
 properties of another class and using them in our class.

 Inheritance can be achieved by deriving a new class from
 existing class.The new class will get the combined features
 of both the classes.


 Polymorphism: The ability to take more than many forms.

 An operation which exhibits diferent behaviours at different
 instances.

-----------------------------------------------------------------------------
 

























 

    






















 




 


 
