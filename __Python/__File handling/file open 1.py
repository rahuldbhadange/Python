'''with open ("C:\Iotic_Labs\rre.txt") as fo:
    print ("Name of the file: ", fo.name)
    print ("Closed or not : ", fo.closed)
    print ("Opening mode : ", fo.mode)
    print ("Softspace flag : ", fo.softspace)

'''

file = open("C:\Iotic_Labs\rre.txt")

data = file.read()

print (data)

file.close()
