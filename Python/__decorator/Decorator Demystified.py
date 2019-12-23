# Decorators demystified
def bread(func):

    def wrapper():
        print("</'''''1'''''\>")
        func()
        print("<\_____5_____/>")
    return wrapper


def ingredients(func):
    def wrapper():
        print('###toma2toes###')
        func()
        print('~~~~sal4ad~~~~')
    return wrapper


def ham(food='-----ham-----'):
    print(food)


# sandwich()


print("\n")
_ham = bread(ingredients(ham))
_ham()


# Using the Python decorator syntax:
print("\n")


@bread  # 1
@ingredients    # 2
def ham_sandwich(food='--ham_3_sandwich--'):
    print(food)


ham_sandwich()


# The order you set the decorators MATTERS:
print("\n")


@ingredients
@bread
def cheese_sandwich(food='cheese_3_sandwich'):
    print(food)


cheese_sandwich()
