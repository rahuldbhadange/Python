def outer():
    x = "local"

    def inner():
        nonlocal x
        x = "nonlocal"
        print("inner:", x)

    inner()
    print("outer:", x)


outer()

print("""
In the above code there is a nested function inner(). 
We use nonlocal keyword to create nonlocal variable. 
The inner() function is defined in the scope of another function outer().

Note : If we change value of nonlocal variable, the changes appears in the local variable.
""")
