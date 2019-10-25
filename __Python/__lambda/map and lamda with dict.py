# Initialize `fahrenheit` dictionary
print("\nexample 4: ")
fahrenheit = {'t1': -30, 't2': -20, 't3': -10, 't4': 0}

# Get the corresponding `celsius` values
celsius = list(map(lambda x: (float(5)/9)*(x-32), fahrenheit.values()))
print(celsius)

# Create the `celsius` dictionary
celsius_dict = dict(zip(fahrenheit.keys(), celsius))
# celsius_dict = zip(fahrenheit.keys(), celsius)

print(celsius_dict)
