x = 0


class Fruit:
    def __init__(self):
        global x
        x += 1  # x == x+1
        print("I'm a fruit")


class Citrus(Fruit):
    def __init__(self):
        super().__init__()
        global x
        x += 2
        print("I'm citrus")

print(x)
