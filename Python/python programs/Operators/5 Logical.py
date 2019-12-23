#Logical operators: They give logical relationship b/w 2 variables

'''Logical operators are
1)and
2)or
3)not

  x            y       x and y     x or y
  True         True    True        True    
  True         False   False       True
  False        True    False       True
  False        False   False       False   '''


x=10
y=4
z=2

p=(x>y) and (y!=z)
print(p)

q=(x==y) and (y==x-6) or (x==y+z+4)
print(q)
