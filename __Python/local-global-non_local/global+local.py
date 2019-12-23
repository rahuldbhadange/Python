x = "global"


def foo():
    global x
    y = "local"
    x = x * 2
    print(x)
    print(y)

print(x)
foo()
print(x)


print("""\n\n
In the above code, we declare x as a global and y as a local variable in the foo(). 
Then, we use multiplication operator * to modify the global variable x and we print both x and y.
After calling the foo(), the value of x becomes global global because we used the x * 2 to print two times global. 
After that, we print the value of local variable y i.e local.
""")
