class A:
    def func(self):
        print("Hi")
    def monkey(self):
        print("Hi, monkey")


m.A.func = monkey
a = m.A()
a.func()
