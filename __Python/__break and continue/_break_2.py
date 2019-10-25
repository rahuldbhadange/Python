"""continue skips the current executing loop and MOVES TO the next loop
whereas break MOVES OUT of the loop and executes the next statement after the loop.
continue causes the program counter to return to the first line of the
loop (the condition is checked and the value of n is increment) and the final value of n is 10
It should also be noted that break only terminates the execution of the loop it is within.
"""
'''
for i in range(10):
    if i == 5:
        break
    print ("[", i, "]")

for i in range(11,20):
    if i == 15:
        continue
    print ("[", i, "]")

'''
for i in range(11,20):
    print ("[", i, "]")
    continue
    # print ("continue")




'''
print(i)
    if i == 5:
        break
sample = range(10) #(1,2,3,4,5,6,7,8,9,0)
next(sample)
'''

n = 0
for i in range(10):
    n = 10
    if i == 5:
        break
    print ("[", i, "]")
    n = n+1
print(n)
