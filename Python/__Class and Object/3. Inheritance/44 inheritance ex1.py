class A:
    a = 10
    b = 20

    def m1(self):
        print("from super class:")
        self.x = 4.5
        print("a=", A.a)
        print("b=", A.b)


class B(A):     # class B extending A
    c = 30
    d = 40

    def m2(self):
        print("from derived class:")
        print("a=", B.a)     # Accessing 'a' of class A using class name
        print("b=", B.b)     # Accessing 'b' of class A
        print("c=", B.c)
        print("d=", B.d)
        self.e = B.a+B.b+B.c+B.d
        print("e=", self.e)
        print("\n\n\n")
        self.m1()      # Accessing method 'm1' of class A
        print("x=", self.x)


b1 = B()
b1.m2()
