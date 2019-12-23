def group_by_owners(files):
    d = {}
    
    for k, v in files.items():
        if v in d:
            d[v].append(k)
        d[v] = list(k)
    
    return d

    
files = {
    'Input.txt': 'Randy',
    'Code.py': 'Stan',
    'Output.txt': 'Randy'
}   
print(group_by_owners(files))