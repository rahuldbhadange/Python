"""
# defining a decorator
- we can wrap a function inside function or class inside class
- we can assign function to a variable, use that variable as function - first class function
- this is helpful when we don't want to change the functionality of the module but need to add some features into it
-
"""


def _decorator(func):   # receiving function as a variable argument
    print('step2')
    # inner is a wrapper function in which the argument is called
    # inner function can access the outer local functions like in this case "func"

    def inner():
        print('step4')
        print("Hello, this is before original function executes.")

        # calling the actual function now, inside the wrapper function.
        func()
        print("Bye !!! This is after original function execution.")
        print('step6')

    # returning function as a variable
    return inner    # (not called yet)


# defining a original function (will be called inside wrapper i.e inner)
@_decorator
def function_to_be_used():
    print("This is an original function !!!")
    print('step5')
    # passing 'function_to_be_used' inside the decorator to control its behavior


print('step1')
# calling function with function as a variable argument
# deco_function_to_be_used_variable = _decorator(function_to_be_used)   # returning function as variable argument
# assigning it to variable


#  calling the function
print('step3')
# deco_function_to_be_used_variable()




function_to_be_used()
