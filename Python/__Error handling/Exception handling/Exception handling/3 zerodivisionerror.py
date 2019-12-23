x=int(input("Enter First No:"))
y=int(input("Enter Second No:"))
try:
      z=x/y
      print(z)
except(ZeroDivisionError):
      print("2nd No cannot be zero")

