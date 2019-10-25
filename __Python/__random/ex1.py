# Python3 program explaining work 
# of randint() function 

# imports random module 
import random 

# Generates a random number between a given positive range

r1 = random.randint(0, 10) 
print("Random number between 0 and 10 is ", r1)

# Generates a random number between 
# two given negative range 
r2 = random.randint(-10, -1) 
print("Random number between -10 and -1 is : ", r2)

# Generates a random number between 
# a positive and a negative range 
r3 = random.randint(-5, 5) 
print("%s is Random number between -5 and 5 ", r3)
