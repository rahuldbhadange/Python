# checking int in the list or not
def find(num, num_list):
    n = len(num_list)
    for i in range(n):
        print(num_list[i] , num)
        if n == num_list[i]:
            return i
            break
    return False
num = 65
num_list = [323,34,235,65,342,453,54,3423]
print(find(num, num_list))


# check that same numerical value present in given two string
# "1abc" and "ab1c"
# 1 is numerical and same value
def check_num(a, b):
    print(a, b)
    for i in range(len(a)):
        for j in range(len(b)):
            print(a[i], b[j])
            if a[i] == b[j] and (a[i] is int) and (b[j] is int):
                print(a[i])
                # yield a[i]
    return None

a, b = "1abc", "ab1c"
result = check_num(a, b)
if result:
    for i in result:
        print(i)
else:
    print("Not Present")
