import json

print(json.dumps({"name": "John", "age": 30}), type({"name": "John", "age": 30}), type(json.dumps({"name": "John", "age": 30})))    # dict->object
print(json.dumps(["apple", "bananas"]), type(["apple", "bananas"]), type(json.dumps(["apple", "bananas"])))     # List -> array
print(json.dumps(("apple", "bananas")))     # Tuple -> array
print(json.dumps("hello"))      # str -> String
print(json.dumps(42))       # int -> Number
print(json.dumps(31.76))    # float -> Number
print(json.dumps(True))     # True -> true
print(json.dumps(False))    # False -> false
print(json.dumps(None))     # None -> null
