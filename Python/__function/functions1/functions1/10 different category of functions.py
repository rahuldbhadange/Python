#1.function with no parameters and with no return type
def sum():
    x=10
    y=20
    z=x+y
    print("sum=",z)
sum()

#2.function with parameters and with no return type
def sum1(a,b):
    c=a+b
    print("sum=",c)
sum1(30,40)

#3.function with parameters and with return type
def sum2(p,q):
    r=p+q
    return r
s=sum2(50,60)
print("sum=",s)

#4.function with no parameters and with return type
def sum3():
    x=70
    y=80
    z=x+y
    return z
m=sum3()
print("sum=",m)



    
