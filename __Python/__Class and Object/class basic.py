class Cal(object):
    # pi is a class variable
    pi = 3.142

    def __init__(self, radius):
        # self.radius is an instance variable
        self.radius = radius

    def area(self):
        return self.pi * (self.radius ** 2)


# object/instance "a"
a = Cal(32)
print(a.area())
# Output: 3217.408
print(a.pi)
# Output: 3.142
a.pi = 43
print(a.pi)
# Output: 43

# object/instance "b"
print("\n")
b = Cal(44)
print(b.area())
# Output: 6082.912
print(b.pi)
# Output: 3.142
b.pi = 50
print(b.pi)
# Output: 50


# There are not many issues while using immutable class variables.
# This is the major reason due to which beginners do not try to learn more about this subject
# because everything works! If you also believe that instance and class variables can not cause any problem
# if used incorrectly then check the next example.
class SuperClass(object):
    superpowers = []

    def __init__(self, name):
        self.name = name

    def add_superpower(self, power):
        self.superpowers.append(power)


foo = SuperClass('foo')
bar = SuperClass('bar')
print(foo.name)
# Output: 'foo'

print(bar.name)
# Output: 'bar'

foo.add_superpower('fly')
print(bar.superpowers)
# Output: ['fly']

print(foo.superpowers)
# Output: ['fly']
# That is the beauty of the wrong usage of mutable class variables.
# To make your code safe against this kind of surprise attacks then make sure that
# you do not use mutable class variables. You may use them only if you know what you are doing.
