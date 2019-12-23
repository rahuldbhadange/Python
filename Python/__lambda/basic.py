"""  syntax: lambda arguments: expression  """


# lambda_function_variable = lambda input : output expression

_double = lambda x: x * 2
print(_double(5), _double)

my_list = [1, 3, 4, 5, 6, 7]
new_list = list(filter(lambda x: (x % 2 == 0), my_list))
print(new_list)

x = lambda a: a + 10

print(x(5))

_list = [6, 1, 2, 3, 4, 5, 65, 4, 7, 9]

# p = list(lambda: 1 if x > 5 else 0, _list)
# print(p)


b = list(filter(lambda a: a > 5, _list))    # providing output for function output True
print(b)

e = filter(lambda a: a % 5 == 0, _list)   # providing output for function output True
print(e, type(e))
for i in e:
    print(i)

c = list(map(lambda a: a + 2, _list))   # providing output wrt function
print(c)

d = map(lambda a: a + 2, _list)
print(d, type(d))
for i in d:
    print(i)
