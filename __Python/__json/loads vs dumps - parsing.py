import json

x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann", "Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(type(x))
print(x)

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(type(y))
print(y)

# parsing JSON result is a Python dictionary
z = json.loads(y)
print(type(z))
print(z)
