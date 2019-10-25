x=10      #global variable

def display1():
    y=20    #local variable
    z=x+y
    print("x=",x)
    print("y=",y)
    print("z=",z)
display1()
print("\n\n")
print("x=",x)
#print("y=",y) #cannot be accessed 
#print("z=",z) #cannot be accessed
