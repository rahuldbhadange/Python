# Okay, still here? Now the fun part...
# You’ve seen that functions are objects. Therefore, functions:
#   can be assigned to a variable
#   can be defined in another function
# That means that a function can return another function. Have a look! ☺


def get_talk(kind='shout'):
    # We define functions on the fly
    def shout(word='yes'):
        return word.capitalize() + '!'

    def whisper(word='yes'):
        return word.lower() + '...'
    # Then we return one of them
    if kind == 'shout':
        # We don’t use '()'. We are not calling the function;
        # instead, we’re returning the function object
        return shout
    else:
        return whisper


# How do you use this strange beast?
# Get the function and assign it to a variable
talk = get_talk()
# You can see that `talk` is here a function object:
# print(talk)
# outputs : <function shout at 0xb7ea817c>

# The object is the one returned by the function:
# print(talk())
# outputs : Yes!

# And you can even use it directly if you feel wild:
print(get_talk('123')())            # important
# outputs : yes...

# But wait...there’s more!
# If you can return a function, you can pass one as a parameter:


def do_something_before(func):
    print('I do something before then I call the function you gave me')
    print(func())


do_something_before(talk)
# outputs:
# I do something before then I call the function you gave me
# Yes!

# Well, you just have everything needed to understand decorators.
# You see, decorators are “wrappers”, which means that they
# let you execute code before and after the function they decorate without modifying the function itself.
