# class MyClass(object):
#     # @staticmethod
#     def the_static_method(x):
#         print(x)
#
#
# MyClass.the_static_method(2)    # outputs 2


# Note that some code might use the old method of defining a static method,
# using staticmethod as a function rather than a decorator.
# This should only be used if you have to support ancient versions of Python (2.2 and 2.3)


class MyClass(object):
    # @classmethod
    @staticmethod

    def the_class_method():
        print("the class method")
    def the_static_method():
        print('k')
    # the_static_method = staticmethod(the_static_method)

MyClass.the_class_method()
MyClass.the_static_method(2)    # outputs 2
print(type(MyClass.the_static_method(5)))
MyClass.the_class_method()
print(type(MyClass.the_class_method()))

# This is entirely identical to the first example (using @staticmethod), just not using the nice decorator syntax

# Finally, use staticmethod() sparingly!
# There are very few situations where static-methods are necessary in Python,
# and I've seen them used many times where a separate "top-level" function would have been clearer.
