# importing libraries 
import time 
import math 


# decorator to calculate duration taken by any function.
def calculate_time(func):
	# added arguments inside the inner1, 
	# if function takes any arguments, 
	# can be added like this. 
	def inner(*args, **kwargs):
		# storing time before function execution
		begin = time.time()
		func(*args, **kwargs)
		# storing time after function execution 
		end = time.time()
		time.sleep(3)
		print("Total time taken by function: ", func.__name__, end - begin)
	return inner


# this can be added to any function present,
# in this case to calculate a factorial 
@calculate_time
def _factorial(num):
	# sleep 2 seconds because it takes very less time 
	# so that you can see the actual difference

	time.sleep(2) 
	print(math.factorial(num)) 


# calling the function.
_factorial(10)
