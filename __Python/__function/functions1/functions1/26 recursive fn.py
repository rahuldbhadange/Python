#Recursive function: A function which is called by itself is known as a recursive function.
x=1
def recur():
    print("hello")
    global x            #forward declaration     
    while(x<=5):
        x=x+1
        recur()
        
recur()
