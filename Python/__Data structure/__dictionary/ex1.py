"""Method	               Description

clear()	        Removes all the elements from the dictionary
copy()	        Returns a copy of the dictionary
fromkeys()	    Returns a dictionary with the specified keys and values
get()	        Returns the value of the specified key
items()	        Returns a list containing a tuple for each key value pair
keys()	        Returns a list containing the dictionary's keys
pop()	        Removes the element with the specified key
popitem()	    Removes the last inserted key-value pair
setdefault()	Returns the value of the specified key. If the key does not exist: insert the key, with the specified value
update()	    Updates the dictionary with the specified key-value pairs
values()	    Returns a list of all the values in the dictionary"""

dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
# Put all keys of `dict1` in a list and returns the list
print(dict1.keys())
# Put all values saved in `dict1` in a list and returns the list
print(dict1.values())
print(dict1.items())


d = {1: 'one', 2: 'two', 3: 'three'}
d1 = d.items()
print(d1, type(d1))
print(d, type(d))
# e = d.items()
# print(e, type(e))


print(d.copy())
e = d.copy()
print(e)


sapwarrantyrecall = [{id:1, "Pnguid":"AFBWiyhYHtiE5aq+SeSqiw=="}, {id:2, "rahul":"AFBWiyhYHtiE5aq+SeSqiw=="}]
nu = sapwarrantyrecall[1]
print(sapwarrantyrecall[0])
