# A static method does not receive an implicit first argument.


"""
Syntax:

class C(object):
    @staticmethod
    def fun(arg1, arg2, ...):
        ...
returns: a static method for function fun.

A static method is also a method which is bound to the class and not the object of the class.
A static method can’t access or modify class state.
It is present in a class because it makes sense for the method to be present in class.
"""


# Python program to demonstrate use of class method and static method.
from datetime import date


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # a class method to create a Person object by birth year.
    @classmethod
    def fromBirthYear(cls, name, year):
        return cls(name, date.today().year - year)

    # a static method to check if a Person is adult or not.
    @staticmethod
    def isAdult(age):
        return age > 18


person1 = Person('sonu', 21)
person2 = Person.fromBirthYear('mayank', 1996)

print(person1.age)
print(person1.name)
print(person2.age)
print(person2.name)

# print the result
# print(Person.isAdult(22))
