try:
    with open("tabs.txt", "r") as f:
        print(f.read())
except IOError:
    print("File not found")
else:
    print("else block")
# finally:
  #  print("finally block")


print("other block")
