class emp:
    def __init__(self, name, sal):
        self.name = name # public var
        self.sal = sal
        self._name = name # private var
        self._sal = sal
        self.__name = name # protected var
        self.__sal = sal

try:
    obj = emp("rahul", 50)
    print(obj.name, obj.sal)
    print(obj._name, obj._sal)
    print(obj._emp__name, obj._emp__sal)
    print(obj.__name, obj.__sal)
except AttributeError:
    print("AttributeError")

    
except Exception as e:
    print(e)
