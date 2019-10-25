n=int(input("enter a no"))
temp=n
sum=0
while(n>0):
    rem=n%10
    fact=1
    while(rem>0):
        fact=fact*rem;
        rem=rem-1
    sum=sum+fact
    n=n//10
if(sum==temp):
    print("Given no is a strong no")
else:
    print("Given no is not a strong no")
