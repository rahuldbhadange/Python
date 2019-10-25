class sample:
    def __init__(self): #constructor
        print("constructor of sample class")
        self.x=10 #constructor initializing 2 NSV's
        self.y=20
        
    def display(self):  #method
        print("method of sample class")
        print(self.x)
        print(self.y)
s1=sample()#whenever object created ,constructor executed automatically 
s1.display()
s1.display()#method called for multiple times
print(s1.x)
print(s1.y)

print("\n\n")
s2=sample()
s2.display()
s2.display()
print(s2.x)
print(s2.y)


