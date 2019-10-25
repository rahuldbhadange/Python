#1.A function can be called any no of times
def display():
    print("Good morning....")
display()
display()
display()
#here 3 fn calls r made,so 3 times the fn is executed





#2.The order in which the functions are defined and the order
 #in which they are called,need not be the same


def English():
    print("ABCDEFGH........")
def maths():
    print("1234567..........")
def chemistry():
    print("H2O is chemical name of water")
chemistry()  # function call
maths()
maths()
English()
#functions will be executed in the order in which the function calls are made.





#3.A function can be called from another function
def Andhra():
    print("hello Amaravathi.....")
def Telangana():
    print("hello hyderabad......")
    Andhra() #Andhra called from Telangana

Telangana()

#4.A function cannot be defined in another function
def display():
    print("hello ......")
    def show():
        print("hai.....")
    show()    
display()
#show()
#Advantage of functions:1.code re-usuability
#                       2.once function is declared,it can be executed for mutiple times





