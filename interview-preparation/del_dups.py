def del_dups(seq):
    seen = {}
    pos = 0
    for item in seq:
        print(seen)
        if item not in seen:
            seen[item] = True
            seq[pos] = item
            pos += 1
    print(seen)
    del seq[pos:]

lst = [8, 8, 9, 9, 7, 15, 15, 2, 2]
del_dups(lst)
print(lst)

lsst = [1, 0, 8, 8, 2]
print(lsst)
lsst[2] = 44
print(lsst)
