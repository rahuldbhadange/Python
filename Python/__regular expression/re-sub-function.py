import re

# Replace every white-space character with the number 9:

str = "The rain in Spain but here it no rain"
x = re.sub("\s", "9", str)
print(x)


# Replace the first 2 occurrences:

str = "The rain in Spain but here it no rain"
x = re.sub("\s", "8989", str, 4)
print(x)
