#Adding static and non-static variables to the class explicitly
class test:
    a=10 #SV
    def __init__(self):
        self.b=20 #NSV
t1=test()
print(test.a)#accessing sv using classname
print(t1.b)  #accessing NSV using Reference variable

test.c=30  #adding new static variable to the class,
           #from outside the class using classname
print(test.c)  

t1.d=40   #adding NSV to the object,
          #from outside the class using Reference variable
print(t1.d)

#creating one more object
t2=test()
print(t2.b) #valid
#print(t2.d) #not valid bcoz d belongs to t1 but not t2
t2.e=50
print(t2.e)


#static variables of class a=10,c=30
#non-static variables b=20,d=40,e=50
#t1 object----->b=20,d=40
#t2 object----->b=20,e=50






        
