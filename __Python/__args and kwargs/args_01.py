import datetime


class __thing_solar(object):

    print("thing_solar class")

    def _test(self):
        print('test method')
        print(datetime.datetime.now())

    def _created_callback(self):
        print('created_callback')
        print(datetime.datetime.now())


solar = __thing_solar()
solar._created_callback()
# print(solar._created_callback())
print(solar._test())
print(solar.test(solar._created_callback()))
# print(solar._created_callback())
