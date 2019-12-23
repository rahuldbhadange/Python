
#parameterized constructor, accepting vaues from keyboard
class customer:
    '''CUSTOMER APPLICATION'''
    bankname="SBI"
    def __init__(self,custname,custaccno,custaddr,cbal):
        self.cname=custname
        self.caccno=custaccno
        self.caddr=custaddr
        self.bal=cbal
    def deposit(self,depositamt):
        self.damt=depositamt
        self.bal=self.bal+self.damt
        print("After depositing",self.damt,"\t","BALANCE=",self.bal)
    def withdraw(self,withdrawamt):
        self.wamt=withdrawamt
        self.bal=self.bal-self.wamt
        print("After withdrawing",self.wamt,"\t","BALANCE=",self.bal)
    def balanceenq(self):
        print("BALANCE:",self.bal)
    def display(self):
        print("CUSTOMER NAME:",self.cname)
        print("ACCOUNT NO:",self.caccno)
        print("ADDRESS:",self.caddr)
        print("BALANCE:",self.bal)
        

print("Enter details of Customer:")
name=input("Enter customer name:")
accno=input("Enter Account no:")
addr=input("enter Address:")

c1=customer(name,accno,addr,30000)
c1.withdraw(5000)
c1.balanceenq()
c1.deposit(10000)
c1.display()







    
        
