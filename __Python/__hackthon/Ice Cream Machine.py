class IceCreamMachine:

    def __init__(self, ingredients, toppings):
        self.ingredients = ingredients
        self.toppings = toppings

    def scoops(self):
        _list = []
        _list_1 = []
        _list_2 = []
        # for i in self.ingredients:
        _list_1.append(self.ingredients[0])
        print(_list_1)
        _list_1.append(self.toppings[0])
        print(_list_1)
        _list.append(_list_1)
        print(_list)
        _list_1.append(self.ingredients[1])
        print(_list_2)
        _list_1.append(self.toppings[0])
        print(_list_2)
        _list.append(_list_2)
        print(_list)
        return _list


machine = IceCreamMachine(["vanilla", "chocolate"], ["chocolate sauce"])
print(machine.scoops())  # should print[['vanilla', 'chocolate sauce'], ['chocolate', 'chocolate sauce']]
