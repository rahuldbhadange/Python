# program illustrating inheritance


class A:
    x = 10

    def __init__(self):
        self.y = 20
        print("constructor of A")

    def _display(self):
        print("Hello....from class A")


class B(A):  # class B extending class A
    z = 30

    def _display2(self):
        print("Hello....from class B")

    def show(self):
        print("x=", B.x)     # Accessing  x of class A, SV accessed using class name
        print("y=", self.y)      # Accessing y of class A, NSV accessed using self
        print("z=", B.z)
        sum = B.x + self.y + B.z
        print("sum=", sum)
        self._display()  # Accessing method of class A using self
        self._display2()     # Accessing method of class B using self


b1 = B()
b1.show()
# b1 address is stored in self of show(), here using self we can also
# access super class properties such as y and display(), bcoz they are
# part of class B
