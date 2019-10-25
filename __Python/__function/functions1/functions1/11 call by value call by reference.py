#call by value: calling a function by providing some values
#call by reference : calling a function by proving some address
def show(x,y):
    z=x+y
    print("sum=",z)
show(10,20)  # call by value

def display(a,b):
    c=a+b
    print("sum=",c)
p=30
q=40
display(p,q)  #call by reference

#when to go for call by reference---->when accepting i/p from keyboard

def putdetails(name,htno,age):
    print("NAME:",name)
    print("HTNO:",htno)
    print("AGE:",age)

name=input("Enter NAME:")
htno=input("Enter HTNO:")
age=int(input("Enter AGE:"))

putdetails(name,htno,age)
