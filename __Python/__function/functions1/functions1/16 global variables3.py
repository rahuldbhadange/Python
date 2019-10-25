#modifying global variables

x=10
def display():
    #I want to modify global variable 'x' value
    global x  #forward declaration for modifying global variable
    x=40
    print(x)
    
def display2():
    print(x)


display2()
display()
display2()
