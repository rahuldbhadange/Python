## fibonacci

a,b = 0,5
for i in range(0,50,5):     # given range for addition (from,upto,interval)
    print('Repeation No.', i)
    print('a', a)
    print('b', b)
    a,b = b,a+b