class student:
    name="Blake"
    rollno=501
    branch="CSE" #here name,rollno,branch are static variables

    def display(self):
        print("name:",student.name)
        print("rollno:",student.rollno)
        print("branch:",student.branch)
s1=student() # s1 is object
s1.display() # displays s1 object properties


        
