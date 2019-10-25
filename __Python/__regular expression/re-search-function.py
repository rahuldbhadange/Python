# The search() Function
# The search() function searches the string for a match, and returns a Match object if there is a match.

import re

# If there is more than one match, only the first occurrence of the match will be returned:
str = "The rain in Spain"
x = re.search("\s", str)  # Note: here "\s" mean white-space

print("The first white-space character is located in position:", x.start())
print(x.end(), x.pos, x.string, x.endpos, x.lastindex)

# If no matches are found, the value None is returned:
str_1 = "The rain in Spain"
x = re.search("Portugal", str_1)
print(x)


print(".", "88\s88", ".")
print("\s")
