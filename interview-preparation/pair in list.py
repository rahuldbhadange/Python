a = [10, 20, 20, 10, 10, 30, 50, 10, 20]

print(a)

count = 0
a.sort()
print(a)

for i in range(len(a)-1):
    if a[i] == a[i+1]:
        count += 1     
    
print(count)
    
