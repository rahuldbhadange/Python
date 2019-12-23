print("\nexample 1: ")

dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
dict2 = {"a": 5, "b": 6, "c": 7, "d": 8}
# Put all keys of `dict1` in a list and returns the list
print(dict2.keys())
# Put all values saved in `dict1` in a list and returns the list
print(dict2.values(), type(dict2.values()))
print(dict2.items())
print(dict1.items())
dict_variable = {key: value for (key, value) in dict1.items()}


print("\nexample 2: ")
dict3 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
# Double each value in the dictionary
double_dict = {k: v*2 for (k, v) in dict3.items()}
print(double_dict)
double_keys = {k*2: v for (k, v) in double_dict.items()}    # using updated dict "double_dict"
print(double_keys)


# Consider the following problem, where you want to create a new dictionary
# where the key is a number divisible by 2 in a range of 0-10 and it's value is the square of the number.

# Let's see how the same problem can be solved using a for loop and dictionary comprehension:
print("\nexample 3: ")
numbers = range(10)
new_dict_for = {}
# Add values to `new_dict` using for loop
for n in numbers:
    if n % 2 == 0:
        new_dict_for[n] = n**2  # appending into empty dict
print(new_dict_for)
# Use dictionary comprehension
new_dict_comp = {n: n**2 for n in numbers if n % 2 == 0}    # option 1  - creating dict
new_dict_comp1 = dict((n, n**2) for n in numbers if n % 2 == 0)     # option 2 - creating dict
print(new_dict_comp)
print(new_dict_comp1)


# Initialize `fahrenheit` dictionary
print("\nexample 4: ")
fahrenheit = {'t1': -30, 't2': -20, 't3': -10, 't4': 0}

# Get the corresponding `celsius` values
celsius = list(map(lambda x: (float(5)/9)*(x-32), fahrenheit.values()))
print(celsius)

# Create the `celsius` dictionary
celsius_dict = dict(zip(fahrenheit.keys(), celsius))
# celsius_dict = zip(fahrenheit.keys(), celsius)

print(celsius_dict)
