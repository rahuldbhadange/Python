# Important Points:

# 1. Key value Change:
# If the value of a certain key is changed,
# the position of the key remains unchanged in OrderedDict.

# A Python program to demonstrate working of key

from collections import OrderedDict

print("\nValue change in Dict:::")
d = {}
print("\nBefore:")

d['a'] = 1
d['b'] = 2
d['c'] = 3
d['d'] = 4
print(d)
for key, value in d.items(): 
	print('Key:', key, ",", 'Value:', value)

print("\nAfter:")
d['c'] = 5
print(d)
# d = OrderedDict(sorted(d.items(), key= lambda x:d[1]))
d = OrderedDict(sorted(d.items(), key= lambda x:x[1]))
for key, value in d.items():
	print('Key:', key, ",", 'Value:', value)

print("\nValue change in OrderedDict:::")

print("\nBefore:")
od = OrderedDict()
od['a'] = 9
od['b'] = 2
od['c'] = 8
od['d'] = 4
for key, value in od.items():
	print(key, value) 

print("\nAfter:")

od['c'] = 5
for key, value in od.items():
	print(key, value)
