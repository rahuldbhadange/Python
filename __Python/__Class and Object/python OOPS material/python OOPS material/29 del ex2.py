class sample:
    pass

s1=sample() #Rc=1
s2=sample() #Rc=1

print(s1)
print(s2)

del s1  # Rc becomes 0,Garbage collector is called, s1 is removed

del s2  # Rc becomes 0,Garbage collector is called, s2 is removed

#print(s1)
#print(s2)
