print("""Adding arguments to decorators is a bit different than you might think it is.
You can’t just do something like @my_decorator(3, ‘Python’)
as the decorator expects to take the function itself as its argument…or can you?""")


def info(arg1, arg2):
    print('Decorator arg1 = ' + str(arg1))
    print('Decorator arg2 = ' + str(arg2))

    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            print('Function {} args: {} kwargs: {}'.format(
                function.__name__, str(args), str(kwargs)))
            return function(*args, **kwargs)
        return wrapper
    return the_real_decorator


@info(3, 'Python')
def doubler(number):
    return number * 2


print(doubler(5))
print("\n\n")
print("""As you can see, we have a function nested in a function nested in a function! How does this work? 
The function argument does not even seem to be defined anywhere. 
Let’s remove the decorator and do what we did before when we created the decorator object:""")
print("\n")


def info(arg1, arg2):
    print('Decorator arg1 = ' + str(arg1))
    print('Decorator arg2 = ' + str(arg2))

    def the_real_decorator(function):
        def wrapper(*args, **kwargs):       # ***important
            print('Function {} args: {} kwargs: {}'.format(
                function.__name__, str(args), str(kwargs)))
            return function(*args, **kwargs)
        return wrapper
    return the_real_decorator


def doubler(number):
    return number * 2


decorator = info(3, 'Python')(doubler)      # ***important


print(decorator(5))
print("\n\n")
print("""This code is the equivalent of the previous code. When you call info(3, ‘Python’), 
it returns the actual decorator function, which we then call by passing it the function, doubler.
 This gives us the decorator object itself, which we can then call with the original function’s arguments.
  We can break this down further though:""")
print("\n")


def info(arg1, arg2):
    print('Decorator arg1 = ' + str(arg1))
    print('Decorator arg2 = ' + str(arg2))

    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            print('Function {} args: {} kwargs: {}'.format(
                function.__name__, str(args), str(kwargs)))
            return function(*args, **kwargs)
        return wrapper
    return the_real_decorator


def doubler(number):
    return number * 2


decorator_function = info(3, 'Python')

print(decorator_function)
actual_decorator = decorator_function(doubler)
print(actual_decorator)
# Call the decorated function
print(actual_decorator(5))


print("\n\n")
print("""Here we show that we get the decorator function object first. 
Then we get the decorator object which is the first nested function in info(), 
namely the_real_decorator(). This is where you want to pass the function that is being decorated. 
Now we have the decorated function, so the last line is to call the decorated function.
I also found a neat trick you can do with Python’s functools  
module that will make creating decorators with arguments a bit shorter:""")
print('\n')























from functools import partial


def info(func, arg1, arg2):
    print('Decorator arg1 = ' + str(arg1))
    print('Decorator arg2 = ' + str(arg2))

    def wrapper(*args, **kwargs):
        print('Function {} args: {} kwargs: {}'.format(
            func.__name__, str(args), str(kwargs)))
        return func(*args, **kwargs)
    return wrapper


decorator_with_arguments = partial(info, arg1=3, arg2='Py')


@decorator_with_arguments
def doubler(number):
    return number * 2


print(doubler(5))
print("\n\n")
print("""In this case, you can create a partial function that takes the arguments 
you are going to pass to your decorator for you. This allows you to pass 
the function to be decorated AND the arguments to the decorator to the same function. 
This is actually quite similar to how you can use functools.partial for passing extra 
arguments to event handlers in wxPython or Tkinter.""")
