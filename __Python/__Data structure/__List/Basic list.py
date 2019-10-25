Ls = [None, 3, 5, None, 6, 9, [5, 6], (8, 9), {8: "hello", 'hi': 8546}]
print(Ls, len(Ls), type(Ls), hex(id(Ls)))


empty_list = []
# for i in Ls:
#     empty_list.append(i)
# print(empty_list, len(empty_list), type(empty_list), hex(id(empty_list)))
# _dict = dict(empty_list)
_dict = {8: "hello", 'hi': 8546}
empty_list.append(_dict)
print(empty_list)
