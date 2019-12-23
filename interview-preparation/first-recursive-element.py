a = "agoifgd dfioohoidfg"
# for i in a:

print(list(a))
print(list(a.strip())[0])




def pro(a,b):
    return a * b


def addd(a,b):
    return a + b

answer=(pro if True else addd)(2,3)
print(answer)
