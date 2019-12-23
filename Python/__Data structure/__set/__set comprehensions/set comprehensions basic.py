# set comprehensions
# They are also similar to list comprehensions. The only difference is that they use braces {}. Here is an example:

squared = {x**2 for x in [1, 1, 2]}
print(squared, type(squared))
# Output: {1, 4}
