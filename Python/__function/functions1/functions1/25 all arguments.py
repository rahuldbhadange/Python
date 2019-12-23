


def display(empid,ename="Miller",sal=30000):#here empid is non-default and ename and sal are default arguments
     print(empid,ename,sal)

#display( )
display(101)
display(102,"Kohli")        #non-keyword arguments
display(103,"Blake",40000)  #non-keyword aguments
display(sal=80000,ename="Reddy",empid=104) #keyword arguments
#display("Blake",50000,106)
display("Blake","sanjay",40000,105)

