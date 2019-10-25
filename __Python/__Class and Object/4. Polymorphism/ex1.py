class Bird:
    # @staticmethod
    def intro(self):
        print("There are many types of birds.")

    def flight(self):
        print("Most of the birds can fly but some cannot. \n")


class Sparrow(Bird):

    def flight(self):
        print("Sparrows can fly. \n")


class Ostrich(Bird):

    def flight(self):
        print("Ostriches cannot fly. \n")


obj_bird = Bird()
obj_spr = Sparrow()
obj_ost = Ostrich()

obj_bird.intro()
obj_bird.flight()

obj_spr.intro()
obj_spr.flight()

obj_ost.intro()
obj_ost.flight()
