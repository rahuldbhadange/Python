def quick_sort(dataset, first, last):

    if first < last:

        pivotidx = partition(dataset, first, last)
        
        quick_sort(dataset, first, pivotidx - 1)
        quick_sort(dataset, pivotidx + 1, last)


def partition(data, first, last):
    pivot = data[first]
    lower = first + 1
    upper = last


    done = False
    while not done:
        while upper >= lower and pivot >= data[lower]:
            lower += 1

        while upper >= lower and data[upper] >= pivot:
            upper -= 1

        if lower > upper:
            done = True
        else:
            temp = data[lower]
            data[lower] = data[upper]
            data[upper] = temp


    temp = data[first]
    data[first] = data[upper]
    data[upper] = temp

    return upper


data = [981,543,685,686,45,234,34,7543,23,874,235,983,624]

print(data)
quick_sort(data, 0, len(data) - 1)
print(data)
