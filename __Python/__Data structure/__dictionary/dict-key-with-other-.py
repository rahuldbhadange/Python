d = {1: "one"}  # dict-key with int
print(d)


d = {"one": "one"}  # dict-key with string
print(d)


d = {("a", 2): "one"}  # dict-key with tuple
print(d, type(d.keys))


try:
    d = {{"one": "one"}: "one"}  # dict-key with dict - not possible
    print(d)
except Exception as ex:
    print(ex)


try:
    d = {{1, 2, 3, 5}: "one"}  # dict-key with set - not possible
    print(d)
except Exception as ex:
    print(ex)


try:
    d = {["a", 2]: "one"}  # dict-key with list - not possible
    print(d)
except Exception as ex:
    print(ex)
