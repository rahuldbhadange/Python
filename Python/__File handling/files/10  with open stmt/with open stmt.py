#The with statement can be used while opening a file, The Advantage of with stmt is
#It takes care of closing a file which is opened by it
#with stmt follows space indentation
with open("sample.txt",mode="w") as f:
    f.write("hello Telangana\n") #file already exists, so it truncates
    f.write("hello Andhra\n")   #if file doesnt exist, it creates a new file

with open("sample.txt",mode="r") as f1:
    print(f1.read())    

      #(or) reading using for loop
with open("sample.txt",mode="r") as f2:
    for line in f2:
        print(line)
