#to overcome above problem,we assign values to q and r using keyword arguments

def display(*p,q,r):
    print(p,type(p))
    print(q,type(q))
    print(r,type(r))
display(10,20,30,q=40,r=50)
display((10,20,30),q=40,r=50)
