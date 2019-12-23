l1 = ["UR","TW","TW","HE","YE","TW","EW","SF","D"]

def rm_dup(l1):
    d1 = {}
    for item in l1:

        if item in d1:
            d1[item] += 1
        else:
            d1[item] = 1
    print(d1)
dup(l1)
