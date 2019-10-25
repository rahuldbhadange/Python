#function to find absolute value of a number
def absolute(x):
    if(x>=0):
        return x
    else:
        return -(x)
p=absolute(10)
print(p)
q=absolute(-20)
print(q)

#here absolute done manually,but we have buit-in fn abs()
print(abs(-40))
#both user-defined and built-in are woking same
