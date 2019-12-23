def unique_names(names1, names2):
    names1.extend(names2)
    # no_dup = names1.unique()

    mylist = list(dict.fromkeys(names1))
    return mylist


names1 = ["Ava", "Emma", "Olivia"]
names2 = ["Olivia", "Sophia", "Emma"]
print(unique_names(names1, names2))  # should print Ava, Emma, Olivia, Sophia


mylist = ["a", "b", "a", "c", "c"]
mylist = list(dict.fromkeys(mylist))
print(mylist)