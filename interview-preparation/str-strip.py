s = "Rahul Bhadange"

def fun_str(s):
    print(s, type(s))
    ss = s.strip(" ")
    print(ss, type(ss))

fun_str(s)



string = ' xoxo love xoxo   '

# Leading whitepsace are removed
print(string.strip())

print(string.strip(' xoxoe'))

# Argument doesn't contain space
# No characters are removed.
print(string.strip('sti'))

string = 'android is awesome'
print(string.strip('an'))
