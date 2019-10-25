# Python program to sort one list using the other list 


def sort_list(list1, list2):
	zipped_pairs = zip(list2, list1)
	# print(zipped_pairs)

	z = [x for _, x in sorted(zipped_pairs)]
	return z 


# driver code
x = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
y = [11, 0, 21, 2, 12, 20, 13, 5, 6]
print(x)
print(y, '\n')
print(sort_list(x, y), '\n\n')


x = ["g", "e", "h", "k", "i", "f", "o", "r", "l", "m", "n", "p", "s"]
y = [10, 1, 11, 0, 21, 2, 12, 20, 13, 5, 8, 55, 6]
print(x)
print(y, "\n")
print(sort_list(x, y))
