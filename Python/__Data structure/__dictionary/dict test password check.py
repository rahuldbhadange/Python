USER_DATA = {"ioticuser": "ioticpassword"}


def verify(username, password):
    print(USER_DATA)
    print(username, password)
    if not (username and password):
        return "empty"
    return USER_DATA.get(username) == password


try:
    print(verify())
except AttributeError:
    print("AttributeError")
except KeyError:
    print("KeyError")
except Exception as Ex:
    print("{}".format(Ex))
