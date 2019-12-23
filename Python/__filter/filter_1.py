"""
The filter() function in Python takes in a function and a list as arguments.
This offers an elegant way to filter out all the elements of a sequence “sequence”,
for which the function returns True.
"""

# filter function takes two args, 1. function and 2. List, the result will be the boolean value True/False.
# function executes the functionality defined in it wrt list elements, returns T/F.

# l1 = [5, 7, 22, 97, 54, 62, 77, 23, 73, 61, 56]
# final_list = list(filter(lambda x: (x % 2 != 0), l1))
# print(final_list)


def squre(list2):
    # l3 = []
    # for i in list2:
    #     l3.append(i+i)
    # print("l3", l3)

    for i in list2:
        return i % 2 != 0
    

l2 = [5, 7, 22, 97, 54, 62]


final_op = list(filter(squre(l2)), l2)
print("final_op", final_op)
