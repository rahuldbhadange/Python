def average_numbers(num_list):
    sum = 0
    num = len(num_list)
    print(num)
    try:
        for i in num_list:
            sum = sum + i
        avg = (sum / num)
        return avg
    except UnboundLocalError as EX:
        print("Error is :", EX)
    except Exception as Ex:
        print(Ex)


my_avg = average_numbers([0.5, 1, 2, 3, 4, 5, 6, 5])
print(my_avg)

