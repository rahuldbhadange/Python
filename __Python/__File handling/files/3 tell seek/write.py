f=open("demo.txt")
print(f.tell())
f.seek(5)
print(f.tell())
print(f.read())
print(f.tell())
f.close()
