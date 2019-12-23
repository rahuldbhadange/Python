# The split() Function
# The split() function returns a list where the string has been split at each match:

import re

# Split at each white-space character:
str = "The rain in Spain"
x = re.split("\s", str)
print(x)

# You can control the number of occurrences by specifying the maxsplit parameter:

# Split the string only at the first occurrence:

str = "The rain in Spain"
x = re.split("\s", str, 1)
print(x)

str = "The rain in Spain"
x = re.split("\s", str, 0)
print(x)

str = "The rain in Spain"
x = re.split("\s", str, 2)
print(x)


str = "The rain in Spain"
x = re.split("\s", str, 10)
print(x)
