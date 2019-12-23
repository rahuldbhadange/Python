class x:
    a=10
    def __init__(self):
        self.b=20
        print("constructor......")
    def m1(self):
        print("from m1....")

class y:
    c=30
    def m2(self):
        print("from m2....")
    def display(self):
        self.d=40
        print(x.a)#Accessing SV of class x using classname
        x1=x() #creating ref_variable of x
        print(x1.b)#Accessing NSV of class x using ref_variable
        print(y.c)#Accessing sv of class y
        print(self.d)#Accessing NSV of class x  
        #we cant access m1()method of class x using self bcoz,
        #self stores address of current class object,so to access m1()
        #of class x,create object of class x and using that ref_variable
        #we can access m1()
        x1.m1()#Accessing m1() of class x using ref_variable
        self.m2()#Accessing m2() of class y using self
y1=y()
y1.display()


        
        
        
