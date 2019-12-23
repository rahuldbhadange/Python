"""class A():
    def __init__(self,parameter):
        self.initialize_parameter=4*parameter

class B(A):
    def __init__(self):
        pass

    def function(self,another_parameter):
        return self.initialize_parameter*another_parameter
But in this case, calling:

B_instance=B()
print B_instance.function(10)"""


class A(object):
    def __init__(self, another_parameter):
        self.initialize_parameter = 4 * another_parameter
        return self.initialize_parameter


class B(A):
    def __init__(self, another_parameter):
        super(A, self).__init__(self, another_parameter)
        # self.another_parameter = another_parameter
    # def function(self, another_parameter):
    #     return self.initialize_parameter * another_parameter


b = B()
print(b(5))

# B_instance = B()
# print(B_instance.function(10))


class A1(object):
    # def __init__(self, arg):
    #     self.arg = arg

    def _mul(self, a):
        self.initialize_parameter = 4 * a
        return self.initialize_parameter


a = A1()
# print(a._mul(5))
