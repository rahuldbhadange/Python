from collections import namedtuple

result=namedtuple('result','Physics Chemistry Maths') # format
Ayushi=result(Physics=86,Chemistry=95,Maths=66) # declaring the tuple
print(Ayushi.Physics)
print(Ayushi.Chemistry)
print(Ayushi.Maths)
