import pprint
stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
print(stuff)
stuff.insert(0, stuff[:])
print(stuff)
pp = pprint.PrettyPrinter(indent=10, depth=3)
pp.pprint(stuff)