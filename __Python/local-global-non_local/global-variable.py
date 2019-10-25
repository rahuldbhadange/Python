# Global in Nested functions
# In order to use global inside a nested functions,
# we have to declare a variable with global keyword inside a nested function

# Python program showing a use of
# global in nested function


def add():
    x = 15

    def change():
        global x
        x = 20

    print("Before making change: ", x)
    print("Making change")
    change()
    print("After making change: ", x)


add()
print("value of x", x)

"""Before making changing:  15
Making change
After making change:  15
value of x 20"""


# In the above example Before and after making change(),
# the variable x takes the value of local variable i.e x = 15.
# Outside of the add() function, the variable x will take value defined in the change() function i.e x = 20.
# because we have used global keyword in x to create global variable inside the change() function (local scope).
