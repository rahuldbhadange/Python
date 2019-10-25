**Global keyword in Python:**
In Python, a variable declared outside of the function or in global scope is known as global variable. 
This means, global variable can be accessed inside or outside of the function.
Global keyword is a keyword that allows a user to modify a variable outside of the current scope. 
It is used to create global variables from a non-global scope i.e inside a function. 
Global keyword is used inside a function only when we want to do assignments or when we want to change a variable. 
Global is not needed for printing and accessing.


**Rules of global keyword:**
- If a variable is assigned a value anywhere within the function’s body, it’s assumed to be a local unless explicitly declared as global.
- Variables that are only referenced inside a function are implicitly global.
- We Use global keyword to use a global variable inside a function.
- There is no need to use global keyword outside a function.