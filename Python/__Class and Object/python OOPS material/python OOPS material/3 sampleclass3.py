
class test:
    """Sample class"""#doc string
    x=10  #static variable
    y=20  #static variables
    #def m1():
   #    print("hello....") #error bcoz it is fn,fn cant b in class
    def m1(self):          #to make fn as method,make it self
        print("x=",test.x) #fuction means we can directly make function call but
        print("y=",test.y)#method, we cant call directly,we need to create object to call it  
        
#end of class
#A class wont execute automatically, we need to create object
#using object only we can access the class members
#how to create object
#syntax:    objectname=classname()
t1=test()
t1.m1()
print(test.x)#static variables accessed by using classname from outside the class
print(test.y)
#print(x) #error bcoz,static variable should be accessed by using classname
#print(y)


#whenever object is created,its address is taken by python interpreter and returns indirect
  #address, which is stored in another variable called reference variable,using this
  #ref variable we access the class members
#creating object of a class
#syntax: objname =classname()
#ex:           t1=test()              ----->here t1 is reference variable
