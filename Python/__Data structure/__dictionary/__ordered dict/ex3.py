# Important Points:

# 2. Deletion and Re-Inserting: Deleting and re-inserting the same key will push it to the back as OrderedDict however maintains the order of insertion.


# A Python program to demonstrate working of deletion 
# re-inserion in OrderedDict

print("\n value change in Dict:")
d = {}
print("\nBefore deleting:\n") 

d['a'] = 1
d['b'] = 2
d['c'] = 3
d['d'] = 4
for key, value in d.items(): 
	print('Key:',key,",",'Value:',value)

print("\nAfter deleting:\n") 
d.pop('c')
for key, value in d.items(): 
	print('Key:',key,",",'Value:',value)

print("\nAfter re-inserting:\n") 
d['c'] = 3
for key, value in d.items(): 
	print('Key:',key,",",'Value:',value)


print("\n value change in OrderedDict:")
from collections import OrderedDict 

print("Before deleting:\n") 
od = OrderedDict() 
od['a'] = 1
od['b'] = 2
od['c'] = 3
od['d'] = 4

for key, value in od.items(): 
	print('Key:',key,",",'Value:',value) 

print("\nAfter deleting:\n") 
od.pop('c') 
for key, value in od.items(): 
	print(key, value) 

print("\nAfter re-inserting:\n") 
od['c'] = 3
for key, value in od.items(): 
	print(key, value) 
