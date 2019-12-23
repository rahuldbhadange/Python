#write mode
f=open("sample.txt",mode="w")
f.write("hello kolkata\n") #file already exists, so it truncates
f.close()              #if file doesnt exist, it creates a new file

f1=open("sample.txt")
print(f1.read())    
f1.close()
