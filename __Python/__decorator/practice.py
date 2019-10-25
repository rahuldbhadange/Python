def test_1(f):
    print("test_1")

    def inside_test_1():
        print("inside_test_1")
        # fuc()
    return inside_test_1

#
# def test_fuc_1():
#     print("test_fuc")


# test_1(test_fuc_1)


def test_2(f):
    print("test_2")

    def inside_test_2():
        print("inside_test_2")
        # fuc()
    return inside_test_2

#
# def test_fuc_2():
#     print("test_fuc_2")


# test_2(test_fuc_2)


# @test_2
# @test_1
def test():
    print("show me functions")


# if __name__ == '__main__':
#     test()

# if __name__ == '__main__':
#     test()
