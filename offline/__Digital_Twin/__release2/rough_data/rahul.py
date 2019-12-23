data = {"col1":"data1a","col2":"data2a"}
name_map = {'col1':'newcol1','col2':'newcol2'}
new_data = dict((name_map[name], val) for name,val in data.items())
print(new_data)
