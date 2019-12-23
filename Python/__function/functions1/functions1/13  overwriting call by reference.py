#call by reference,overwriting the reference
def display(list):
    list=[1,2,3,4,5]
    print(list)
    print(id(list))
list = [10,20,30,40,50]
print(list)
display(list)
print(list)
print(id(list))


    



