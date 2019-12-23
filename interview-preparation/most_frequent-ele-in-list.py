# Program to find most frequent 
# element in a list

def most_frequent(List): 
	dict = {} 
	count, itm = 0, '' 
	for item in reversed(List): 
		dict[item] = dict.get(item, 1) + 1
		if dict[item] >= count : 
			count, itm = dict[item], item 
	return(itm)

List = [2, 1, 2, 2, 1, 3, 3, 3] 
print(most_frequent(List))
