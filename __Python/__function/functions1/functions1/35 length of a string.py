#function to find the length of a string
def mylen(s):
    count=0
    for p in s:
        count=count+1
    return count
x="hadoop"
print(mylen(x))#userdefined

print(len(x))#built in
#both userdefined and builtin are working same


