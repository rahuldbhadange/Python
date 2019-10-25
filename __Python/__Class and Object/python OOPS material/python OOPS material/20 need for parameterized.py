#disadvantage of default constructor

class student:
    def __init__(self):
        self.name="Ajay"
        self.age=25
s1=student()
print(s1.name) #default values
print(s1.age)
s1.name="sanjay" #modified values
s1.age=27
print(s1.name)
print(s1.age)


s2=student()
print(s2.name) #default values
print(s2.age)
s2.name="Dhoni"  #modified values
s2.age=40
print(s2.name)
print(s2.age)
#Here evertime the constructor is initializing the NSV's with same
#values, but i want different values for each object during object
#creation only,then go for parameterized constructor,which specifies
#different values for each object.









