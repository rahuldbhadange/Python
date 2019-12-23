tu = (1, 3, 4, [23,34,54])
print(type(tu), type(tu[3]), tu)

tu[3][2] = 2
print(type(tu), type(tu[3]), tu)
tu[2] = 1111
print(type(tu), type(tu[3]), tu)
