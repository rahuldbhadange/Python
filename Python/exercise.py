# Question:
# Write a program which will find all such numbers which are divisible by 7 but are not a multiple of 5,
# between 2000 and 3200 (both included).
# The numbers obtained should be printed in a comma-separated sequence on a single line.
#
# Hints:
# Consider use range(#begin, #end) method
#
# Solution:


# _list = []
#
# for i in range(2000, 3201):
#     if (i % 7 == 0) and (i % 5 != 0):
#         _list.append(str(i))
# print(_list)
# print(','.join(_list))


#
# Question:
# Write a program which can compute the factorial of a given numbers.
# The results should be printed in a comma-separated sequence on a single line.
# Suppose the following input is supplied to the program:
# 8
# Then, the output should be:
# 40320
#
# Hints:
# In case of input data being supplied to the question, it should be assumed to be a console input.

# Solution:


def fact(x):
    if x == 0:
        return 1
    return x * fact(x - 1)


x = int(input())
print(fact(x))


# ----------------------------------------#
# Question:
#
# Write a program to solve a classic ancient Chinese puzzle:
# We count 35 heads and 94 legs among the chickens and rabbits in a farm.
# How many rabbits and how many chickens do we have?
#
# Hint:
# Use for loop to iterate all possible solutions.
#
# Solution:


# rabbits: 4
# chickens: 2
# heads: 35
# legs: 94

# (How much * 2) rabbits] + [(How much * 4) chickens] = 94

def solve(numheads, numlegs):
    ns = 'No solutions!'
    for i in range(numheads + 1):
        # print(i)
        j = numheads - i
        # print(j)
        if 2 * i + 4 * j == numlegs:
            return i, j
    return ns, ns


numheads = 35
numlegs = 94
solutions = solve(numheads, numlegs)
print(solutions)

# ---------------------------------------- #


# Question:
#
# Please write a program which prints all permutations of [1,2,3]
#
#
# Hints:
# Use itertools.permutations() to get permutations of list.
#
# Solution:



import itertools

print(list(itertools.permutations([1, 2, 3])))


print(complex(-5))


class emp:

    var = "jhhj"

    def __init__(self):
        self.har = "kjfksd"

    def fcuk(self):
        print("kj")
        self.gar = "kjhfkjsd"

        print(self.har)


obj = emp()
obj.fcuk()
print(obj.var)
print(obj.gar)
print(obj.har)


from array import array as arr

my_array = arr("l", [5, 85, 74, 5, 5, 56, 4])
print(my_array[::-1])


from random import shuffle


x = ['Keep', 'The', 'Blue', 'Flag', 'Flying', 'High']
shuffle(x)
print(x)

# ['The', 'Blue', 'Keep', 'Flag', 'Flying', 'High']