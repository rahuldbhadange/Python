# from .Handcrafted_Decorators import func
from Handcrafted_Decorators import deco as d
from practice import test_2, test_1
__deco = d()


# @func
@__deco.my_shiny_new_decorator
def another_stand_alone_function():
    print('Leave me alone')


another_stand_alone_function()


# @test_2
# @test_1
# def test():
#     print("show me functions")


# test()
