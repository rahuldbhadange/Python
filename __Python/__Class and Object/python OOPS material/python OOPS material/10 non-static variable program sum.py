#program illustrating non-static variable(NSV)
class sum:
    
    def display(self): #here each object address is passed to self  
        self.x=10 #non-static variable
        self.y=20 #non-static variable
        print("x=",self.x) #accessing and printing non-static variable
        print("y=",self.y)
        print("sum=",self.x+self.y)
s1=sum() #creating ref variable s1 which stores indirect address of object.
print(s1) #prints indirect address of object s1
s1.display() #using object accessing class members
print(s1.x)#acessing NSV from outside the class using object
print(s1.y)
s1.x=30
print(s1.x)
print(id(s1.x))

s2=sum() #creating 2nd object
print(s2)
s2.display()
s2.x=40
print(s2.x)
print(id(s2.x))

#static variables related to class
#non-static variable related to object
#NSV can be accesed within the class using self
#NSV can be accessed from outside the class using object

#SV can be accesed inside/outside the class using classname
