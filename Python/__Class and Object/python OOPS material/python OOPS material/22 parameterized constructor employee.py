class employee:
    """employee Application"""
    company="Infosys"  #static variable
    empcount=0
    def __init__(self,empname,empid,empsal,design): 
   #how many constructor parameters are defined,those many
   #NSV's should be defined
        #data 
        self.empname=empname
        self.empid=empid
        self.empsal=empsal
        self.design=design
        employee.empcount=employee.empcount+1
        
    def displayemployee(self):
        print("NAME:",self.empname,"ID:",self.empid,"SALARY:",self.empsal,
              " DESIGNATION:",self.design)
#end of class
emp1=employee("Scott",101,30000.00,"Manager")
emp2=employee("Miller",102,40000.00,"Clerk")
emp3=employee("Blake",103,50000.00,"Developer")

emp1.displayemployee()
emp2.displayemployee()
emp3.displayemployee()

print("Total No of Employees are:",employee.empcount)
print("COMPANY NAME:",employee.company)





              
              
