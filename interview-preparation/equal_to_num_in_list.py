def equal_to_num_in_list1(list1, num):
    d = {}
    for i in range(len(list1)):
        if (num - list1[i]) in d.keys():
            print(list1[i], d.keys())
            return True
        d[list1[i]] = 1
    return False


list1 = [-1,10,3,4,7,5,5,8,2,9,1]
num = 10
print(equal_to_num_in_list1(list1, num))



def equal_to_num_in_list(list1, num):
    for i in range(len(list1)-2):
        for j in range(len(list1)-1):
            if (list1[i] + list1[j]) == num:
                print(list1[i], list1[j])
                # return True
    return False
   
list1 = [-1,10,3,4,7,5,5,8,2,9,1]
num = 10
print(equal_to_num_in_list(list1, num))
    
 
