def odds(n):
    odd = [i for i in range(n+1) if i%2!=0]
    for i in odd:
        yield i
for i in odds(8):
    print(i)

# result = odds(45)
# for i in result:
  #  print(i)
