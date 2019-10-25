''' Read input from STDIN. Print your output to STDOUT '''
    #Use input() to read input from STDIN and use print to write your output to STDOUT


def main():
    Z = input("Please Enter the element you wish to know ASCII value: \n")
    print("The ASCII value of '" + Z + "' is", ord(Z))


# main()
print("Welcome !")
for i in range(5):
    Q = input("Press 'C' to continue OR 'Enter' to exit:  \n")
    if Q == 'C':
        main()
    else:
        exit()
