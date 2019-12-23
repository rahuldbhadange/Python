# List comprehensions provide a short and concise way to create lists.
# It consists of square brackets containing an expression followed by a for clause,
# then zero or more for or if clauses. The expressions can be anything,
# meaning you can put in all kinds of objects in lists.
# The result would be a new list made after the evaluation of the expression in context of the if and for clauses.

# Blueprint
# variable = [out_exp for out_exp in input_list if out_exp == 2]
# Here is a short example:

# example 1:
multiples = [i for i in range(1, 31) if i % 3 == 0]
print(multiples)
# Output: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]

# This can be really useful to make lists quickly.
# It is even preferred by some instead of the filter function.
# List comprehensions really shine when you want to supply a list to a method
# or function to make a new list by appending to it in each iteration of the for loop.

# For instance you would usually do something like this:
squared = []
for x in range(10):
    squared.append(x**2)
print(squared)
# You can simplify it using list comprehensions. For example:
squared = [x**2 for x in range(10)]
print(squared)
