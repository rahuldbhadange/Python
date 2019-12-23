class customer:
    """customer Application"""
    bankname="SBI"  #static variable
    def __init__(self,custname,accno,addr,bal): 
   #how many constructor parameters are defined,those many
   #NSV's should be defined
        #data 
        self.custname=custname
        self.accno=accno
        self.addr=addr
        self.bal=bal
    #operations
    def deposit(self,depositamt):
        self.bal=self.bal+depositamt
        
    def withdraw(self,withdrawamt):
        self.bal=self.bal-withdrawamt
        
    def balenq(self):
        print("Balance:",self.bal)
        
    def display(self):
        print("Customer Name:",self.custname)
        print("Account No:",self.accno)
        print("Address:",self.addr)
        print("Balance:",self.bal)
c1=customer("scott",5230143,"Ameerpet",60000.00)
c1.deposit(20000.00)
c1.withdraw(10000.00)
c1.balenq()
c1.deposit(30000.00)
c1.withdraw(20000.00)
c1.display()
print("Bank name:",customer.bankname)

print("\n\n\n")
c2=customer("Blake",6230143,"Chennai",40000.00)
c2.deposit(20000.00)
c2.withdraw(10000.00)
c2.balenq()
c2.deposit(30000.00)
c2.withdraw(20000.00)
c2.display()
print("Bank name:",customer.bankname) 

#Here if customer withdrawing more than available balance
#then he should be restricted by using exception handling
#i.e displaying "Insufficient funds"






              
              
