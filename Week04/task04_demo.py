from task04_h_matrix_operator import Matrix, MatrixOperator

def main():
    #Get the first matrix 
    print("Let's do the entry for the first matrix")
    matrix1 = Matrix()
    matrix1.get_matrix_input()

    #Get the second matrix
    matrix2 = None
    another_matrix = input("Do you have another matrix. Press 'y' if there is: ")
    if another_matrix == 'y':
        matrix2 = Matrix()
        matrix2.get_matrix_input()

    print("Matrix 1\n=======")
    matrix1.print_matrix()

    matrix_op = MatrixOperator()

    #Transpose
    matrix_transpose = matrix_op.get_transpose(matrix1)
    print("\n\nTranspose of Matrix 1:")
    matrix_transpose.print_matrix()

    #Complex conjugate
    matrix_cc = matrix_op.complexconjugate(matrix1)
    print("\n\nComplex conjugate of Matrix 1:")
    matrix_cc.print_matrix()

    det = matrix_op.determinant(matrix1)
    print(f"\n\nDeterminant of Matrix 1: {det.cartesian_form_compact()}")
    matrix_i = matrix_op.inverse(matrix1)
    print("Inverse of Matrix 1:")
    matrix_i.print_matrix()

    #Conjugate transpose
    matrix_ct = matrix_op.get_transpose(matrix_cc)
    print("\n\nConjugate transpose or adjoint of Matrix 1:")
    matrix_ct.print_matrix()

    if matrix2 is not None:
        print("\n\nMatrix 2\n=======")
        matrix2.print_matrix()

        #Transpose
        matrix_transpose = matrix_op.get_transpose(matrix2)
        print("\n\nTranspose of Matrix 2:")
        matrix_transpose.print_matrix()

        #Complex conjugate
        matrix_cc = matrix_op.complexconjugate(matrix2)
        print("\n\nComplex conjugate of Matrix 2:")
        matrix_cc.print_matrix()

        det = matrix_op.determinant(matrix2)
        print(f"\n\nDeterminant of Matrix 2: {det.cartesian_form_compact()}")
        matrix_i = matrix_op.inverse(matrix2)
        print("Inverse of Matrix 2:")
        matrix_i.print_matrix()

        #Conjugate transpose
        matrix_ct = matrix_op.get_transpose(matrix_cc)
        print("\n\nConjugate transpose or adjoint of Matrix 2:")
        matrix_ct.print_matrix()

        #Addition
        matrix_addition = matrix_op.add(matrix1, matrix2)
        print("\n\nAddition of Matrix 1 and Matrix 2:\n===============")
        matrix_addition.print_matrix()

        #Subtraction
        matrix_subtraction = matrix_op.subtract(matrix1, matrix2)
        print("\n\nSubtraction of Matrix 2 from Matrix 1:\n===============")
        matrix_subtraction.print_matrix()

        #Multiplication
        matrix_multiplication = matrix_op.multiply(matrix1, matrix2)
        print("\n\nMultiplication of Matrix 1 and Matrix 2:\n===============")
        matrix_multiplication.print_matrix()

        #Inner product
        innerproduct = matrix_op.innerproduct(matrix1, matrix2)
        print("\n\nInner product of Matrix 1 and Matrix 2:\n===============")
        print(f"{innerproduct.cartesian_form_compact()}")

        #Tensor product
        matrix_tensorproduct = matrix_op.tensorproduct(matrix1, matrix2)
        print("\n\nTensor product of Matrix 1 and Matrix 2:\n===============")
        matrix_tensorproduct.print_matrix()

'''
    if matrix2 == None:
        print("Matrix\n=======")
        matrix1.print_matrix()
    else:
        print("Matrix 1\n=======")
        matrix1.print_matrix()
        print("\n\nMatrix 2\n=======")
        matrix2.print_matrix()

    
    if matrix2 == None: #Only single-parameter operations will be done
        #Transpose
        matrix_transpose = matrix_op.get_transpose(matrix1)
        print("\n\nTranspose:")
        matrix_transpose.print_matrix()

        #Complex conjugate
        matrix_cc = matrix_op.complexconjugate(matrix1)
        print("\n\nComplex conjugate:")
        matrix_cc.print_matrix()

        det = matrix_op.determinant(matrix1)
        print(f"\nDeterminant: {det.cartesian_form_compact()}")
        matrix_i = matrix_op.inverse(matrix1)
        print("\nInverse:")
        matrix_i.print_matrix()

        #Conjugate transpose
        matrix_ct = matrix_op.get_transpose(matrix_cc)
        print("\n\nConjugate transpose or adjoint:")
        matrix_ct.print_matrix()
    else: #All available operations will be done
        #Transpose
        matrix_transpose = matrix_op.get_transpose(matrix1)
        print("\n\nTranspose of Matrix 1:\n===============")
        matrix_transpose.print_matrix()
        matrix_transpose = matrix_op.get_transpose(matrix2)
        print("\n\nTranspose of Matrix 2:\n===============")
        matrix_transpose.print_matrix()

        #Complex conjugate
        matrix_cc = matrix_op.complexconjugate(matrix1)
        print("\n\nComplex conjugate:")
        matrix_cc.print_matrix()

        det = matrix_op.determinant(matrix1)
        print(f"\nDeterminant: {det.cartesian_form_compact()}")
        matrix_i = matrix_op.inverse(matrix1)
        print("\nInverse:")
        matrix_i.print_matrix()

        #Conjugate transpose
        matrix_ct = matrix_op.get_transpose(matrix_cc)
        print("\n\nConjugate transpose or adjoint:")
        matrix_ct.print_matrix()
'''
        
if __name__ == "__main__":
    main()