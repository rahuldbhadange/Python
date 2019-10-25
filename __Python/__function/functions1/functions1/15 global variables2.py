x=10

def display1():
    x=20
    print(x) #local variable will be given preference

def display2():
    print(x)

display1()
display2()
