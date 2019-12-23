def date_int(takeoff, landing):
    if landing > takeoff:
        return landing - takeoff
    elif takeoff > landing:
        return 24 + landing - takeoff
print("")


if __name__ == '__main__':
     t = int(input("enter t : "))
     l = int(input("enter l : "))
     res = date_int(t, l)
     print("Output is {}".format(res))
