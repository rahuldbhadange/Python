from collections.abc import Iterable

def flatten_the_nested_list(List):
    """Yield items from any nested iterable; see Reference."""
    for element in List:
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            for sub_ele in flatten_the_nested_list(element):
                yield sub_ele
        else:
            yield element

l = [['1','3'],['34','45',['65','232',['7','9'],'33'],['45','78'],'997'],'232',['64','534','85'],'5436','2342']
print(list(flatten_the_nested_list(l)))
