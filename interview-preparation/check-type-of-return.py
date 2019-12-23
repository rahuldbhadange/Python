def check():
    x = {'a': 1, }
    y = {}
    a = [{}]
    return a, {**x, **y}

z = check()
print(z, type(z))


a = "dfsa", ["ew", "yesar"]
print(a, type(a))
