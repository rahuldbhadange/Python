class customer:
    x=10
    cname=input("ENTER CUSTOMER NAME:")
    accno=input("ENTER ACCOUNT NO:")
    bal=float(input("ENTER BALANCE:"))
    def display(self):
        print("x=",customer.x)
        print("NAME:",customer.cname)
        print("ACCNO:",customer.accno)
        print("BALANCE:",customer.bal)
c1=customer()
customer.x=20
c1.display()




    
    
