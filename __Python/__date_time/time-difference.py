from datetime import datetime
s1 = '10:33:26'
s2 = '11:15:49' # for example
FMT = '%H:%M:%S'
tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
print(tdelta)

# d1, m1, y1 = [int(x) for x in input("Please Enter The Start Time for {} Show of {} Case (HH:MM:SS) : \n").split(':')]
# print(d1, m1, y1)