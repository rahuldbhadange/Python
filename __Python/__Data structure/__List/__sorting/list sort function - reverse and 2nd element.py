numbers = [1, 3, 4, 2] 
# Sorting list of Integers in ascending 
numbers.sort() 
print(numbers)

numbers = [1, 3, 4, 2] 
# Sorting list of Integers in descending 
numbers.sort(reverse=True)
print(numbers) 


# Python program to demonstrate sorting by user's choice:
# function to return the second element of the two elements passed as the parameter
def sort_second(val):
	return val[1]


# list1 to demonstrate the use of sorting using using second key
list1 = [(7, 2), (6, 3), (89, 1), (5, 4), (9, 5)]
print(type(list1))

# sorts the array in ascending according to second element
list1.sort(key=sort_second)		# "reverse=False" by default
print(list1)

# sorts the array in descending according to second element
list1.sort(key=sort_second, reverse=True)
print(list1) 

# sorts the array in descending according
list1.sort(reverse=False)
print(list1)

list1.sort()
print(list1)

list1.sort(reverse=True)
print(list1)
