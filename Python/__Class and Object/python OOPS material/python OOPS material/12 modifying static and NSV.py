#program for modifying static and non-static variable
class sample:
    a=4.5#static variable
    b=2.6#static variable
    def display(self):
        self.x=10 #non-static variable
        self.y=20 #non-static variable
        print("x=",self.x) 
        print("y=",self.y)
        print("a=",sample.a)
        print("b=",sample.b)
        #modifying the values
        self.x=self.x+50
        self.y=self.y+60
        sample.a=sample.a+70
        sample.b=sample.b+80
        print("x=",self.x) 
        print("y=",self.y)
        print("a=",sample.a)
        print("b=",sample.b)
        
s1=sample()
print(s1) #prints indirect address of object 
s1.display() #using object accessing class member

s2=sample() #creating 2nd object
print(s2)
s2.display()
        
        
        
