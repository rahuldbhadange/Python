#string methods

#1.s.upper()
x="hyderabad"
print(x.upper())

#2.s.lower()
x="GOOD MORNING123 *"
print(x.lower())

#3.replace()
x="java is easy"
print(x.replace("java","Python"))

#4.Split()
line="python is simple"
print(line)
print(type(line))

words=line.split(" ")
print(words)
print(type(words))

#5.strip()---> Removes whitespaces before and after the string
x="     Python is easy        "
print(x.strip())

#6.startswith()
#  endswith()
x="python is simple"
print(x.startswith("python"))
print(x.endswith("simple"))

#7.find()
x="python is simple"
print(x.find("python"))

#8.count()
x="hello hello hello how r u?"
print(x.count("hello"))
print(x.count("h"))

#9.capitalize()----->converts 1st character of a string to capital case
x="hyderabad"
print(x.capitalize())


#String Functions

#1.len()
x="hello"
print(len(x))

#2.max()----->returns highest character
x="hello"
print(max(x))

#3.min()
print(min(x))



#string special operators

#1)+ : concatenation
x="hello world"
print(x[0:6] + "India")

#2)* : for repeatition

x="hello"
print(x*3)

#3)[ ]: for indexing

#4)[ : ] : for slicing

#5) in
#6) not in

x="python"
print('p' in x)
print('a' not in x)
































































