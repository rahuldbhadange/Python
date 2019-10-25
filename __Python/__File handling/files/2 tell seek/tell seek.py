#tell() , seek()

f=open("sample.txt")
print(f.tell())
print(f.read())
f.seek(8)
print(f.tell())
print(f.read())
print(f.tell())
f.seek(11)
print(f.read(4)) #reads 4 characters from current position
f.close() 

