class student:
    name=input("Enter name:")
    rollno=int(input("Enter Rollno:"))
    marks=int(input("Enter marks:"))

    def display(self):
        print("NAME:",student.name)
        print("ROLLNO:",student.rollno)
        print("MARKS:",student.marks)
s1=student()
s1.display()
print(student.name)
print(student.rollno)
print(student.marks)
