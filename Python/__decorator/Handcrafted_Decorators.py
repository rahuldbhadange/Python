# Handcrafted decorators

# How you’d do it manually:


class deco(object):
    # A decorator is a function that expects ANOTHER function as parameter
    # @staticmethod
    # def my_shiny_new_decorator(a_function_to_decorate):
    def my_shiny_new_decorator(self, a_function_to_decorate):
        print("inside my_shiny_new_decorator")
        # Inside, the decorator defines a function on the fly: the wrapper.
        # This function is going to be wrapped around the original function
        # so it can execute code before and after it.

        def the_wrapper_around_the_original_function():
            # Put here the code you want to be executed BEFORE the original
            # function is called
            print('Before the function runs')
            # Call the function here (using parentheses)
            a_function_to_decorate()
            # Put here the code you want to be executed AFTER the original
            # function is called
            print('After the function runs')
        # At this point, `a_function_to_decorate` HAS NEVER BEEN EXECUTED.
        # We return the wrapper function we have just created.
        # The wrapper contains the function and the code to execute before
        # and after. It’s ready to use!
        return the_wrapper_around_the_original_function


# class deco1():
def func(fun):
    print("inside deco1/func")
    def fun1():
        print("inside deco1/func1")
        fun()
        print("after")
    return fun1


# def another():
#     print("another")


__deco = deco()
# __deco1 = deco1()


# Now imagine you create a function you don’t want to ever touch again.
# def a_stand_alone_function():
#     print('I am a stand alone function, don’t you dare modify me')


# a_stand_alone_function()
# outputs: I am a stand alone function, don't you dare modify me

# Well, you can decorate it to extend its behavior.
# Just pass it to the decorator, it will wrap it dynamically in
# any code you want and return you a new function ready to be used:
# a_stand_alone_function_decorated = __deco.my_shiny_new_decorator(a_stand_alone_function)
# a_stand_alone_function_decorated()

# 4/12/2019 The best explanation of Python decorators I’ve ever seen. (An archived answer from StackOverflow.)
# https://gist.github.com/Zearin/2f40b7b9cfc51132851a 4/15

# outputs:
# Before the function runs
# I am a stand alone function, don't you dare modify me
# After the function runs

# Now, you probably want that every time you call a_stand_alone_function , a_stand_alone_function_decorated is called
# instead. That’s easy, just overwrite a_stand_alone_function with the function returned by my_shiny_new_decorator :
# a_stand_alone_function = __deco.my_shiny_new_decorator(a_stand_alone_function)
# a_stand_alone_function()
# outputs:
# Before the function runs
# I am a stand alone function, don’t you dare modify me
# After the function runs
# And guess what? That’s EXACTLY what decorators do!


@func
@__deco.my_shiny_new_decorator
def another_stand_alone_function():
    print('Leave me alone')


if __name__ == '__main__':
    another_stand_alone_function()

print("hello")

# The previous example, using the decorator syntax:
# @my_shiny_new_decorator
# def another_stand_alone_function():
#     print('Leave me alone')
# another_stand_alone_function()
# outputs:
# Before the function runs
# Leave me alone
# After the function runs
# Yes, that’s all, it’s that simple. @decorator is just a shortcut to:
# another_stand_alone_function = my_shiny_new_decorator(another_stand_alone_function)
# Decorators are just a pythonic variant of the decorator design pattern.
# There are several classic design patterns embedded in
# Python to ease development (like iterators).
# Of course, you can accumulate decorators:
