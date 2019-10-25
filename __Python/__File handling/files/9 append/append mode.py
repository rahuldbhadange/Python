#append mode
f=open("sample.txt",mode="a")
f.write("hello banglore \n") #if file already exists, it appends
f.close()              #if file doesnt exist, it creates a new file
                       #if the program executed for 5 times,5 times appended
f1=open("sample.txt")
print(f1.read())    
f1.close()
