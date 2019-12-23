#Parameterized constructor: A constructor with parameters is called as
#parameterized constructor

class student:
    def __init__(self,name,age): #parameterized constructor
        self.stdname=name
        self.stdage=age
    def display(self):
        print("NAME:",self.stdname)
        print("AGE:",self.stdage)
s1=student("Ajay",25)
s1.display()
s2=student("vijay",28)
s2.display()
s3=student("kohli",26)
s3.display()

#Note: whenever object is created,it is initializing NSV's with
#different values
