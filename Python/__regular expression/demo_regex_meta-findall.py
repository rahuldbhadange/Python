print("\nRegular Expression: \n")

import re


print()
str = "The rain in Spain"
print("""# Find all lower case characters alphabetically between "a" and "m":
        \nInput: {}""".format(str))
x = re.findall("[a-p]", str)
print("""Code: x = re.findall("[a-p]", str)""")
print("Output: ", x)


print()
print()
str_d = "That will be 59 dollars but I need 20"
print("""# Find all digit characters:
        \nInput: {}""".format(str_d))

x = re.findall("\d", str_d)
print("Output: ", x)


print()
print()
str_f = "hell8o world"
print("""# Search for a sequence that starts with "he", followed by two (any) characters, and an "o":
        \nInput: {}""".format(str_f))
w = re.findall("he..8...", str_f)
x = re.findall("he.....", str_f)
y = re.findall("h....o...", str_f)
z = re.findall("he..", str_f)
print("Output: ", w, x, y, z)


print()
print()
str_start = "hello world"
print("""# Check if the string starts with 'hello': 
        \nInput: {}""".format(str_start))
x = re.findall("^hello", str_start)
print("Output: ", x)
if x:
  print("Yes, the string starts with 'hello'")
else:
  print("No match")


print()
print()
str_end = "hello world"
print("""# Check if the string ends with 'world':
        \nInput: """.format(str_end))

x = re.findall("world$", str_end)
print("Output: ", x)
if x:
  print("Yes, the string ends with 'world'")
else:
  print("No match")



print()
print()
str_at_least_one = "The rain in Spain falls mainly in the plain!"
print("""# Check if the string contains "ai" followed by 0 or more "x" characters: 
        \nInput: {}""".format(str_at_least_one))
x = re.findall("aix*", str_at_least_one)
print("Output :", x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")


print()
print()
str_zero_or_more = "The rain in Spain falls mainly in the plain!"
print("""# Check if the string contains "ai" followed by 0 or more "x" characters: 
        \nInput: {}""".format(str_zero_or_more))
x = re.findall("ai0*", str_zero_or_more)
print("Output: ", x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")


print()
print()
str_at_least_one = "The rain in Spain falls mainly in the plain!"
print("""# Check if the string contains "ai" followed by 1 or more "x" characters:
        \nInput: {}""".format(str_at_least_one))
x = re.findall("aix+", str_at_least_one)
print("Output: ", x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")


print()
print()
str_specific = "The rain in Spain falls mainly in the plain!"
print("""# Check if the string contains "a" followed by exactly two "l" characters:
        \nInput: {}""".format(str_specific))
x = re.findall("al{2}", str_specific)
print("Output: ", x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")


print()
print()
str_contains_either_or = "The rain in Spain falls mainly in the plain!"
print("""# Check if the string contains either "falls" or "stays":
    \nInput: {}""".format(str_contains_either_or))

x = re.findall("falls|stays", str_contains_either_or)
print("Output: ", x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")
