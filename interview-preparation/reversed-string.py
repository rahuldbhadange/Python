def reversed_string(data):
    r = ""
    for i in range(len(data)-1, -1, -1):
        r = r + data[i]
        print(r)
    print(r)
    return r

data = "jvifhiiegw"
print(reversed_string(data))


def reversed_string(data):
    r = ""
    for i in data:
        r = i + r
        print(r)
    print(r)
    return r

data = "jvifhiiegw"
print(reversed_string(data))


    
def reversed_string(data):
    out_len = len(data)
    out = [None] * out_len
    print(out)
    out_id = out_len - 1
    for i in data:
        out[out_id] = i
        out_id -=1
        print(out)
    return ''.join(out)

data = "jvifhiiegw"
print(reversed_string(data))
