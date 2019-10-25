#opening a file and reading
f=open("demo1.txt",mode="r") #whenever we call open fn,it internally create file object
print(f.read())
f.close()

#if we use f.close(),the object which is created is going to be
#deleted and other persons can use the file
