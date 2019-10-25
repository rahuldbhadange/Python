from collections import OrderedDict


student_class = {"Ramesh": 560, "Amit": 925, "Harshal": 698, "Uday": 950, "Lokesh": 792,
                 "Bhavin": 258, "Hansika": 988, "Anuradha": 842}


print("Before - Actual data \n", student_class, "\n")


student_clas = OrderedDict(student_class)
print("OrderedDict()---\n", student_clas, type(student_clas), "\n")


std_class = student_class.items()
print("items()---\n", std_class, type(std_class), "\n")

std_class_key = student_class.keys()
print("keys()---\n", std_class_key, "\n")

std_class_val = student_class.values()
print("values()---\n", std_class_val, type(std_class_val), "\n")
for i in std_class_val:
    print(i)


# dict comprehension
# student_class = dict(sorted(student_class.items(), key=lambda x:x[1]))
student_class = dict(sorted(student_class.items(), key=lambda x:x[0]))
# student_class = OrderedDict(sorted(student_class.items(), key=lambda x:x[0]))
print("\nSorted according to marks---\n", student_class, "\n")

for k, v in student_class.items():
    print(k, "has got", v, "marks.", "\n")
    if v >= 950:
        print("Congratulation !!!", k, ".", "well done !!!",  "\n",)
