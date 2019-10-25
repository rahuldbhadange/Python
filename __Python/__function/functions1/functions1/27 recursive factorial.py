#factorial program using recursive function

def fact(n):
    if(n==1):
        return 1
    else:
        return(n*fact(n-1))  #recursive function call

    
num=int(input("enter a number:"))
if(num >= 1):
    print("Factorial of",num,"is",fact(num))
