#Employee application to perform various operations such as
# DA(),TA(),HRA(),PF(),tax()

class employee:
    """employee Application"""
    company="Infosys"  #static variable
    empcount=0
    def __init__(self,empname,empid,empsal,design): 
   #how many constructor parameters are defined,those many
   #NSV's should be defined
    #data (NSV's)
        self.empname=empname
        self.empid=empid
        self.empsal=empsal
        self.design=design
        employee.empcount+=1
    #operations     
    def da(self,daamt):
        self.empsal=self.empsal+daamt
        
    def hra(self,hraamt):
        self.empsal=self.empsal+hraamt
        
    def ta(self,taamt):
        self.empsal=self.empsal-taamt
        
    def pf(self,pfamt):
        self.empsal=self.empsal-pfamt
        
    def tax(self):
        if((self.empsal>250000)&(self.empsal<500000)):
            self.empsal=self.empsal-self.empsal*0.10
            print("Salary after tax Reduction=",self.empsal)
        elif((self.empsal>500000)&(self.empsal<1000000)):
            self.empsal=self.empsal-self.empsal*0.20
            print("Salary after tax Reduction=",self.empsal)
        elif(self.empsal>1000000):
            self.empsal=self.empsal-self.empsal*0.30
            print("Salary after tax Reduction=",self.empsal)
    
     
    def displayemployee(self):
        print("NAME:",self.empname,"ID:",self.empid,"SALARY:",self.empsal,
              "DESIGNATION:",self.design)
        
emp1=employee("Scott",101,300000.00,"Manager")
emp1.da(1500)
emp1.hra(3000)
emp1.ta(2000)
emp1.pf(1200)
emp1.displayemployee()
emp1.tax()

emp2=employee("Miller",102,100000.00,"Clerk")
emp2.da(1100)
emp2.hra(2000)
emp2.ta(1000)
emp2.pf(700)
emp2.displayemployee()
emp2.tax()
print("Total No of Employees are:",employee.empcount)
print("COMPANY NAME:",employee.company)





              
              
