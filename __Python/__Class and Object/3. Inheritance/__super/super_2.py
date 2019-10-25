class Father(object):
    def __init__(self, name, _function):
        self._function()
        print("He is a", name)


class Son(Father):
    def __init__(self, _function):
        print("My father's name is Dilip Bhadange")
        super().__init__('Govt Servant', _function)


def function():
    print("Hello")


s = Son(function)
