#program to access static and non-static variable from outside the class
class sample:
    a=4.5
    b=2.6
    def display(self):
        self.x=10 #non-static variable
        self.y=20 #non-static variable
        
        
s1=sample() #here no NSV's ,bcoz values will be allocates when method is executed
s1.display()#now values allocated and stored in an object and object in-direct address stored in reference variable 
print(sample.a)#static variable accessed using class name 
print(sample.b)

print(s1.x)#NSV accessed using reference variable
print(s1.y)#if we execute these 2 stmts without executing s1.display()method
         #we get error bcoz values wont be allocated,so call s1.dispaly() first
         #To overcome this, allocate values for NSV during object creation only
         #using constructor
        
        
