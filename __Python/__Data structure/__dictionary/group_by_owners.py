import operator


def group_by_owners(files):
    print(files, type(files))
    for k, v in files.items():
        # for v in k:
        print(k, v)
        # if k[v] == k[v]:
        #     print("same", v)
    for f in files:
        print(f[0])
        for g in v:
            print(g)
    _files = sorted(files.items(), key=operator.itemgetter(1), reverse=False)
    print("Sorted: ", _files, type(_files))

    # files = files.items()
    # print(files, type(files))

    # return None


files = {
    'Input.txt': 'Randy',
    'Code.py': 'Stan',
    'Output.txt': 'Randy'
}
print(group_by_owners(files))
