##fizzBuzz


for num in range(0, 16):        # range starts with 0 and ends with 16
    if num % 5 == 0 and num % 3 == 0:       # symbol '%' gives a reminder as a output
        print("fizzBuzz")
    elif num % 5 == 0:
        print('fizz')
    elif num % 3 == 0:
        print('Buzz')
    else:
        print(num)