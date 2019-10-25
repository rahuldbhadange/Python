#without lamda fn, passing one fn as a parameter to another fn

def f1(x):
    print(x)
def f2():
    x=10
    y=20
    z=x+y
    print(z)
    return z
f1(f2())



    
          
