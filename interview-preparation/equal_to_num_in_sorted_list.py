def equal_to_num_in_sorted_list(list1, num):
    low = 0
    high = len(list1) - 1
    while low < high:
        print(list1[low], list1[high])
        suum = list1[low] + list1[high]
        if suum == num:
            return True
        elif suum > num:
            high = high - 1
        elif suum < num:
            low = low + 1
    return False
        
list1 = [-1,4,7,8,9]
num = 10
print(equal_to_num_in_sorted_list(list1, num))
    
