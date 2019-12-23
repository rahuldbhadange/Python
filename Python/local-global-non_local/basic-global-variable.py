# Python program to modify a global
# value inside a function


x = 15
print("x =", x)


def change():
    # using a global keyword
    global x
    # increment value of a by 5
    x = x + 5
    print("Value of x inside change() function :", x)


change()
print("Value of x outside change() function :", x)

print("""\n\n
In the above example, we first define x as global keyword inside the function change(). 
The value of x is then incremented by 5, ie. x=x+5 and hence we get the output as 20.
As we can see by changing the value inside the function change(), 
the change is also reflected in the value outside the global variable.
""")
