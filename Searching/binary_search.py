arr = [1, 2, 3, 4, 5, 7, 10, 22, 33, 44, 55, 66, 77, 78, 88, 99, 111]
right = len(arr) - 1
left = 0
num = 88


def binary_search(arr, num, left, right):

	mid = left + (right - left) // 2
	print(arr, num, left, right, mid)

	if right >= left:

		if arr[mid] == num:
			return mid

		elif arr[mid] > num:
			return binary_search(arr, num, left, mid-1)

		else:
			return binary_search(arr, num, mid+1, right)

	return -1


result = binary_search(arr, num, left, right)

if result == -1:
	print("Not Exists")
else:
	print("The number is found at index {}".format(result))
