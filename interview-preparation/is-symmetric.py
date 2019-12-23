# Efficient Python code for check a matrix is symmetric or not. 
# Returns True if matrix [N][N] is symmetric, else False 

def isSymmetric(mat, N):
    # i == j == 0
    for i in range(N):
        print("i",i)
        # j == i
        for j in range(i, N):
            print("j",j)
            print(mat[i][j], mat[j][i])
            if (mat[i][j] != mat[j][i]):
                return False
    return True



# Driver code 
mat = [[ 1, 3, 5, 5 ],
       [ 3, 9, 4, 14 ],
       [ 5, 4, 9, 0 ],
       [ 5, 4, 0, 0 ]] 

if (isSymmetric(mat, 4)):
    print("Yes")
else:
    print("No")

# This code is contributed by Sachin Bisht 
