#Anonymous function/Lambda function:

 #A function which doesnt have any name,is called lambda fn or Anonymous function

   # syntax: lambda arguments:expression
   
# how to call lambda function?
# Ans: Assign lambda function to a variable,this variable behaves like fn name
        #using that variable name,we can call lambda fn

#ex: function to square a no
f1=lambda x:x*x
p=f1(10)
print(p)
q=f1(20)
print(q) 

#The above code is equivalent to the following code
def f2(x):
    return(x*x)
p=f2(10)
print(p)
q=f2(20)
print(q)


print("\n\n")
#ex:2
f1=lambda x,y:x*y
p=f1(10,20)
print(p)
q=f1(20,30)
print(q) 




