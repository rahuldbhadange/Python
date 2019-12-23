def find_missing(full, partial):
    # for i in full
    item = set(full) - set(partial)
    if item:
        return item
    return None


l1 = [4,12,9,5,6]
l2 = [4,9,12,6]
print(find_missing(l1, l2))
    
