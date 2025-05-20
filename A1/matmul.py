import numpy as np

def is_matrix(a):
    '''
    Check if the matrix is valid
    
    1) It should be a 2D matrix
    2) All rows must have the same number of elements
    3) All the elements must be an integer, float or a complex number
    4) The matrix cannot be empty : [[]]
    
    If the matrix is not of appropriate dimensions value error is raised
    If the matrix has invalid datatypes (string, tuple, etc.) type error is raised
    
    If the matrix is valid then the function returns True without raising any error
    
    '''
    
    # ensure that the matrix is not empty
    if len(a) == 0:
        raise ValueError("Invalid Matrix Dimensions")
    
    # iterate through the rows
    for row in a:
        
        # each row should be a list
        if not isinstance(row,list):
            raise TypeError("Input should be a 2D matrix")
        
        # the row shouldn't be empty and all the rows must have the same length
        if len(row)==0 or len(row) != len(a[0]):
            raise ValueError("Invalid Matrix Dimensions")
        
        #each element should be an integer, float or a complex number
        for element in row:
            if not (isinstance(element, int) or isinstance(element,float) or isinstance(element,complex)):
                raise TypeError("Matrix has invalid datatypes")
    
    # return true if the matrix satisfies all the conditions
    return True


def check_inputs(a, b):
    '''
    Check if the matix are valid and have compatible dimensions
    
    that is, 
    number of columns in first matrix = number of rows in second matrix
    
    '''
    
    # call the is_matrix function 
    is_matrix(a)
    is_matrix(b)
    
    #check the compatibility of the matrices
    if len(a[0]) != len(b):
        raise ValueError("Matrices have incompatible dimensions")


def matrix_multiply(a, b):
    '''
    Perform Matrix Multiplication
    
    Parameters : 
    Matrices to be multiplied - a and b
    
    Returns :
    Product of the matrices - a.b
    
    If the matrices are invalid or imcompatible, raise Error
    
    Matrix multiplication is perfomed with nested for loops
    
    '''
    
    # call check_inputs function to validate the matrices and check compatiblity
    check_inputs(a, b)
    
    m = len(a)      # number of rows in a
    n = len(a[0])   # number of columns in a = number of rows in b
    k = len(b[0])   # number of columns in b
    
    #create an empty matrix of dimensions mxk to store the product
    c = [[0 for _ in range(k)] for _ in range(m)]
    
    #iterate through each element of c
    for i in range(m):
        for j in range(k):
            #calculate the value of element as the dot product of the ith row of a and jth column of b
            c[i][j] = sum(a[i][p] * b[p][j] for p in range(n))
            
    #return the product matrix
    return c
