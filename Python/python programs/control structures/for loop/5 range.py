#Range()function: It is a pre-defined function, whose range starts from
# 0 to given value(excluding)
#ex:- range(10)--->here values from 0 to 9 are generated and stored in an object.

x=range(10)
print(x)
print(type(x))
for p in x:
    print(p)

    
y=range(10,20)
print(y)
print(type(y))
for q in y:
    print(q)
    
z=range(20,30,2)
print(z)
print(type(z))
for r in z:
    print(r)
    
w=range(40,30,-1)
print(w)
print(type(w))
for s in w:
    print(s)
    
