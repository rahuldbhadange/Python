#program to print multiplication table of a number

n=int(input("Enter a no:"))
print("MULTIPLICATION TABLE IS:")
i=1
while(i<=10):
    res=n*i
    print(n,"*",i,"=",res)
    i=i+1
