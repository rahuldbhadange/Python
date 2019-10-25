class test:
    def __init__(self):
        print("constructor called")
    def __del__(self):
        print("destructor called")
t1=test()
t2=test()
t3=test()
print(t1)
print(t2)
print(t3)

x=[t1,t2,t1,t3,t1] #RC of t1=4,Rc of t2=2,Rc of t3=2
   #x[0]=t1,x[2]=t1,x[4]=t1
del x[1] #RC of t2 decreases to 1
print(t2)
del t2  #Rc of t2 decreases to 0,destructor called,t2 removed
#print(t2)
del x[0] #Rc of t1 decreases to 3
del x[0] #Rc of t1 decreases to 2
del x[1] #Rc of t1 decreases to 1
del t1   #Rc of t1 decreases to 0,destructor called,t1 removed
#print(t1)
