print("""
Global variables across python modules :
The best way to share global variables across different modules within the same program is 
to create a special module (often named config or cfg). 
Import the config module in all modules of your application; the module then becomes available as a global name. 
There is only one instance of each module and so any changes made to the module object get reflected everywhere. 
For Example, sharing global variables across modules
""")


# Code 1: Create a config.py file to store global variables:

x = 0
y = 0
z ="none"


# Code 2: Create a modify.py file to modify global variables:

import config
config.x = 1
config.y = 2
config.z ="geeksforgeeks"

# Here we have modified the value of x, y, and z.
# These variables were defined in the module config.py,
# hence we have to import config module and we can use config.variable_name to access these variables.


# Code 3: Create a main.py file to modify global variables:

import config
import modify
print(config.x)
print(config.y)
print(config.z)
