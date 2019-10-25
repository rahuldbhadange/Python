print("""
super() lets you avoid referring to the base class explicitly,
which can be nice. . But the main advantage comes with multiple inheritance, 
where all sorts of fun stuff can happen.
""")


class Mammal(object):
    def __init__(self, mammal_name):
        print("and")
        print(mammal_name, 'is a warm-blooded animal.')


class Cat(Mammal):
    def __init__(self):
        print("Cat has four legs.")
        super().__init__("Cat")


class Dog(Mammal):
    def __init__(self):
        print('Dog has four legs.')
        super().__init__('Dog')


d1 = Dog()
c1 = Cat()
