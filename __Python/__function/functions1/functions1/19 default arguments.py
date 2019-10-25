#2.Default arguments: providing default arguments in function definition,

#if values not specified during fn call,then these r taken as default arguments 
def display(name="john",result="fail"):  #in fn call if values are not specified then by default these values r taken
    print(name,result)
display("Ajay","pass")
display("miller")
display()
