# Decorators are very powerful and useful tool in Python since
# it allows programmers to modify the behavior of function or class.
# Decorators allow us to wrap another function in order to extend the behavior of wrapped function,
# without permanently modifying it.


def hello_decorator(fun):
	print("Outside")

	def inside():
		print("Start")
		fun()
		print("End")
	return inside


@hello_decorator
# 'Above code is equivalent to - hello_decorator = gfg_decorator(hello_decorator)'''
def _hello():
	print("Main")


_hello()

