def unique_names(names1, names2):
    print(names1, names2)
    
    d = {}
    
    for i in range(len(names1)-1):
        if names1[i] in d:
            d[names1[i]] += 1
        d[names1[i]] = 1
            
    for j in range(len(names2)-1):
        if names2[j] in d:
            d[names2[j]] += 1
        d[names2[j]] = 1
    
    print(d)
                
    for k,v in d.items():
        if v == 1:
            yield k
    return None


names1 = ["Ava", "Emma", "Olivia"]
names2 = ["Olivia", "Sophia", "Emma"]
print(list(unique_names(names1, names2))) # should print Ava, Emma, Olivia, Sophia