import os
os.chdir("C:\work\Python")

# file = open('array.txt')
with open("array.txt") as file1:
    for line in reversed(list(file1)):
        # print(line)
        print(line.rstrip())

# file.close()


