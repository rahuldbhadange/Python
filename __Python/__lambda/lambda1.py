"""Lambda definition does not include a “return” statement,
it always contains an expression which is returned.
We can also put a lambda definition anywhere a function is expected,
and we don’t have to assign it to a variable at all."""


def func(a, b):
    c = a * b
    return c


print(func(2, 3), type(func), hex(id(func)))


def cube(y):
    return y * y * y
    # yield y * y * y


print(cube(5), type(cube), hex(id(cube)))
x = lambda x: x * x * x

print(x(6), type(x), hex(id(x)))

