# Reduce is a really useful function for performing some computation on a list and returning the result.
# It applies a rolling computation to sequential pairs of values in a list.
# For example, if you wanted to compute the product of a list of integers.
#
# So the normal way you might go about doing this task in python is using a basic for loop:


product = 1
_list = [1, 2, 3, 4]
for num in _list:
    product = product * num
print(product)

# product = 24

# Now let’s try it with reduce:

from functools import reduce

product = reduce((lambda x, y: x * y), [1, 2, 3, 4])
print(product)

# Output: 24


print(reduce(list.__add__, [[1, 2, 3], [4, 5], [6, 7, 8]], []))


print(int("".join(map(str, [1, 2, 3, 4, 5, 6, 7, 8]))))

print(reduce(lambda a, d: 10*a+d, [1, 2, 3, 4, 5, 6, 7, 8], 0))

