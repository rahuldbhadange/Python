#program illustrating non-static variable(NSV)
class emp:
    company="Infosys" #SV
    def getdetails(self):
        self.ename=input("Enter employee name:")
        self.eid=int(input("Enter empid:"))
        self.esal=int(input("Enter empsal:"))
        self.desig=input("Enter designation:")
    def putdetails(self):
        print("Ename:",self.ename) 
        print("Eid:",self.eid)
        print("Esal:",self.esal)
        print("Designation:",self.desig)
        print("Company:",emp.company)
e1=emp()
e1.getdetails()
e1.putdetails()


e2=emp()  
e2.getdetails()
e2.putdetails()
    
        
