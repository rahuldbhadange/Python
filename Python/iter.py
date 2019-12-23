from collections import Iterable

l = [[[1,2,5,9],[3,8]],[5,0,7],[4,2,6]]

def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x

res = flatten(l)
print(res)
result = []
for i in res:
    result.append(i)
print(result)




import operator
from functools import reduce
print(reduce(operator.concat, l))
