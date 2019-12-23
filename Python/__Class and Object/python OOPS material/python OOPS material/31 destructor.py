class test:
    def __init__(self):
        print("constructor called")
    def __del__(self):
        print("destructor called")
    
t1=test() #RC=1
t2=test() #RC=1
t3=test() #RC=1
print(t3)
t3=test() #If same ref variable is used,then RC decreases by 1
          #RC=0(if same variable is used,RC becomes less i.e 0
          #,so destructor called
          #previous t3 object is destroyed,destructor called
          #and a new t3 object is created.
print(t3)


