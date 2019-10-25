#method with parameters and constructors with parameters

class test:
    def __init__(self,m,n):
        self.x=m
        self.y=n
        print("x=",self.x)
        print("y=",self.y)
    def m1(self,a,b):
        self.p=a
        self.q=b
        print("p=",self.p)
        print("q=",self.q)
x1=test(10,20)
x1.m1(30,40)
