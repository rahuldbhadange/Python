# Python program showing to modify
# a global value without using global
# keyword

a = 15


# function to change a global value
def change():
    # increment value of a by 5
    a = a + 5
    print(a)


print("""This output is an error because we are trying to assign a value to a variable in an outer scope. 
        This can be done with the use of global variable.
        UnboundLocalError: local variable 'x' referenced before assignment
        """)

change()
