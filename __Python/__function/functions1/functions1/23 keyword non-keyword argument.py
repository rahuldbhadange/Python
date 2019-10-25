#3.keyword arguments: During fn call,using parameter name,passing value
#4.non-keyword arguments:During fn call,without parameter name,passing value

def display(branch,code):
    print(branch,code)
display("CSE","05")  #non-keyword argument
display(branch="ECE",code="04") #keyword argument (using parameter name)
display(code="02",branch="EEE") #keyword argument


#display(code="12","IT")

#default and non-default related to fn definition
#key-word and non-keyword relatd to fn call
#Note: After keyword argument,we cannot have nonkeyword argument

