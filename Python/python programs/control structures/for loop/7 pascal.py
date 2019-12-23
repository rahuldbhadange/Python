#program for pascal triangle
n=40 
for i in range(1,11):   #for no of rows 
    print(' '*n,end='') #repeat space for n times
    print('* '*(i))
    n=n-1
