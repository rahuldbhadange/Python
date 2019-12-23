file = "interview.txt"
file_open = open (file, mode = 'r')
file_read = file_open.read()
print(file_read)
file_open.close()


read = "tim.txt"
with open (read, mode='r') as file:
    print(file.read())


