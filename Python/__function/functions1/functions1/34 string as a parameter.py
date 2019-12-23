#passing string as a parameter to function

#built-in function list()takes sting as a parameter an returns list object
x=list("hello")
print(x)
print(type(x))
print(len(x))

#now user defined function taking string as a parameter and returns list object
y=[]
def newlist(s):
    for p in s:
        y.append(p)
    return y
z=newlist("hello")
print(z)
print(type(z))
print(len(z))

#here both built-in and user-defined functions are working samely
