from task04_h_complex_operator import ComplexNumber, ComplexNumberOperator, ComplexNumberForm

class Matrix:
    def __init__(self, row = 1, col = 1, tag = ""):
         #Dimension of the matrix
        self.no_of_rows = row
        self.no_of_columns = col

        self.tag = tag
        
        #Elements of the matrix
        self.elements = []
        for i in range(self.no_of_rows):
            tmp_array = []
            for j in range(self.no_of_columns):
                tmp_array.append(0)
            self.elements.append(tmp_array)


    @property
    def row_dimension(self):
        return self.no_of_rows
    

    @property
    def column_dimension(self):
        return self.no_of_columns
    

    def get_matrix_input(self):
        try:
            self.no_of_rows = int(input("What is the number of rows for this matrix:"))
            self.no_of_columns = int(input("What is the number of columns for this matrix:"))
        except Exception as x:
            print(f'Error while getting matrix input {x}')

        if self.no_of_columns is None:
            self.no_of_columns = 1
        if self.no_of_rows is None:
            self.no_of_rows = 1
        self.elements = []
        for i in range(self.no_of_rows):
            tmp_array = []
            for j in range(self.no_of_columns):
                tmp_array.append(0)
            self.elements.append(tmp_array)

        for i in range(self.no_of_rows):
            tmp_array = []
            for j in range(self.no_of_columns):
                complex_num = ComplexNumber()
                complex_num.get_input(f"Give the matrix element at {i+1}x{j+1}:")
                self.elements[i][j] = complex_num


    def get_row(self, idx):
        if idx >= 0 and idx < self.no_of_rows:
            return self.elements[idx]
        return None
    

    def get_column(self, idx):
        ret = []
        for i in range(self.no_of_rows):
            ret.append(self.get_element(i, idx))
        return ret
    
        
    def get_element(self, row_idx, col_idx):
        if row_idx >= 0 and row_idx < self.no_of_rows and col_idx >= 0 and col_idx < self.no_of_columns:
            return self.elements[row_idx][col_idx] 
        return None
    

    def set_row(self, idx, values):
        if idx >= 0 and idx < self.no_of_rows and len(values) == self.no_of_columns:
            self.elements[idx] = values

    
    def set_column(self, idx, values):
        if idx >= 0 and idx < self.no_of_columns and len(values) == self.no_of_rows:
            row_idx = 0
            for value in values:
                self.set_element(row_idx, idx, value)
                row_idx = row_idx + 1


    def set_element(self, row_idx, col_idx, value):
        if row_idx >= 0 and row_idx < self.no_of_rows and col_idx >= 0 and col_idx < self.no_of_columns:
            self.elements[row_idx][col_idx] = value
        

    def print_matrix(self):
        if self.no_of_rows == 0: #The matrix has no data
            print(self.tag)
        else:    
            for i in range(self.no_of_rows):
                if i > 0:
                    print("")
                for j in range(self.no_of_columns):
                    if i == (self.no_of_rows - 1) and j == (self.no_of_columns - 1):
                        print(self.elements[i][j].cartesian_form_compact())
                    else:
                        print(self.elements[i][j].cartesian_form_compact(), end="")


class MatrixOperator:
    @staticmethod
    def get_transpose(m: Matrix):
        matrix_result = Matrix(m.column_dimension, m.row_dimension)
        for i in range(m.row_dimension):
            matrix_result.set_column(i, m.get_row(i))
        return matrix_result
        

    '''
    def get_transpose(self, idx):
        matrix_result = Matrix()
        if idx == 0 and self.matrix1 is not None:
            matrix_result = Matrix(self.matrix1.column_dimension, self.matrix1.row_dimension)
            for i in range(self.matrix1.row_dimension):
                matrix_result.set_column(i, self.matrix1.get_row(i))
        elif idx == 1 and self.matrix2 is not None:
            matrix_result = Matrix(self.matrix2.column_dimension, self.matrix2.row_dimension)
            for i in range(self.matrix2.row_dimension):
                matrix_result.set_column(i, self.matrix2.get_row(i))
        return matrix_result
    '''
    
    @staticmethod
    def complexconjugate(m: Matrix) -> Matrix:
        matrix_result = Matrix(m.row_dimension, m.column_dimension)
        for i in range(m.row_dimension):
                row = m.get_row(i)
                j = 0
                for ele in row:
                    matrix_result.set_element(i, j, ComplexNumberOperator.conjugate(ele))
                    j = j + 1

        return matrix_result  
    
    '''
    def complexconjugate(self, idx) -> Matrix:
        matrix_result = Matrix()
        matrix_to_use = None
        if idx == 0 and self.matrix1 is not None:
            matrix_to_use = self.matrix1
        elif idx == 1 and self.matrix2 is not None:
            matrix_to_use = self.matrix2

        if matrix_to_use is not None:    
            matrix_result = Matrix(matrix_to_use.row_dimension, matrix_to_use.column_dimension)
            for i in range(matrix_to_use.row_dimension):
                row = matrix_to_use.get_row(i)
                j = 0
                for ele in row:
                    matrix_result.set_element(i, j, ComplexNumberOperator.conjugate(ele))
                    j = j + 1

        return matrix_result   
    '''

    @staticmethod
    def add(m1: Matrix, m2: Matrix) -> Matrix:
        if m1.column_dimension == m2.column_dimension and m1.row_dimension == m2.row_dimension:
            matrix_result = Matrix(m1.row_dimension, m1.column_dimension)
            for i in range(m1.row_dimension):
                for j in range(m1.column_dimension):
                    matrix_result.set_element(i, j, ComplexNumberOperator.add(m1.get_element(i,j), m2.get_element(i,j)))
            return matrix_result        
        return Matrix(0, 0, "Matrix addition can be done ONLY for the matrices of same dimension")
    

    @staticmethod
    def subtract(m1: Matrix, m2: Matrix) -> Matrix:
        if m1.column_dimension == m2.column_dimension and m1.row_dimension == m2.row_dimension:
            matrix_result = Matrix(m1.row_dimension, m1.column_dimension)
            for i in range(m1.row_dimension):
                for j in range(m1.column_dimension):
                    matrix_result.set_element(i, j, ComplexNumberOperator.subtract(m1.get_element(i,j), m2.get_element(i,j)))
            return matrix_result        
        return Matrix(0, 0, "Matrix subtraction can be done ONLY for the matrices of same dimension")
    

    @staticmethod
    def multiply(m1: Matrix, m2: Matrix) -> Matrix:
        if m1.column_dimension == m2.row_dimension:
            matrix_result = Matrix(m1.row_dimension, m2.column_dimension)
            #Initialize all elements as 0 + 0i 
            for i in range(m1.row_dimension):
                for j in range(m2.column_dimension):
                    matrix_result.set_element(i, j, ComplexNumber(ComplexNumberForm.Cartesian, 0,0))

            for i in range(m1.row_dimension):
                for j in range(m2.column_dimension):
                    m1_row = m1.get_row(i)
                    m2_col = m2.get_column(j)
                    tmp_product = matrix_result.get_element(i, j)
                    for k in range(len(m1_row)):
                        tmp_product = ComplexNumberOperator.add(tmp_product, ComplexNumberOperator.multiply(m1_row[k], m2_col[k]))
                    matrix_result.set_element(i, j, tmp_product)
            return matrix_result        
        return Matrix(0, 0, "Matrix multiplication can be done ONLY when the column size of Matrix 1 is equal to the row size of Matrix 2")


    @staticmethod
    #Frobenius inner product
    def innerproduct(m1: Matrix, m2: Matrix): 
        if m1.column_dimension == m2.column_dimension and m1.row_dimension == m2.row_dimension:
            complex_result = ComplexNumber(ComplexNumberForm.Cartesian, 0, 0)
            for i in range(m1.row_dimension):
                for j in range(m1.column_dimension):
                    complex_result = ComplexNumberOperator.add(complex_result, ComplexNumberOperator.multiply(
                        m1.get_element(i, j), m2.get_element(i, j)
                    ))
            return complex_result

        return ComplexNumber(None, None, None, "Inner product can be calculated ONLY when the two matrices have the same dimension")
        
    @staticmethod
    def tensorproduct(m1: Matrix, m2: Matrix): 
        matrix_result = Matrix(m1.row_dimension * m2.row_dimension, m1.column_dimension * m2.column_dimension)
        for i in range(m1.row_dimension):
            for j in range(m1.column_dimension):
                for k in range(m2.row_dimension):
                    for l in range(m2.column_dimension):
                        ele1 = m1.get_element(i, j)
                        ele2 = m2.get_element(k, l)
                        matrix_result.set_element(k + (i * m2.row_dimension), 
                                                  l + (j * m2.column_dimension), 
                                                  ComplexNumberOperator.multiply(ele1, ele2))
        return matrix_result
    
    @staticmethod
    def inverse(m: Matrix):
        if m.row_dimension != m.column_dimension:
            return Matrix(0, 0, "No inverse: not a square matrix")
        det = MatrixOperator.determinant(m)
        if det.is_zero:
            return Matrix(0, 0, "No inverse: not an invertible matrix")
        if det.is_invalid:
            tag_info = det.tag_info
            if len(tag_info) > 0:
                return Matrix(0, 0, tag_info)
            return Matrix(0, 0, "No inverse: not an invertible matrix")
        cofm = MatrixOperator.cofactor(m)
        cofm_t = MatrixOperator.get_transpose(cofm)
        for i in range(cofm_t.row_dimension):
            for j in range(cofm_t.column_dimension):
                cofm_t.set_element(i, j, ComplexNumberOperator.divide(cofm_t.get_element(i, j), det))
        return cofm_t
                

    @staticmethod
    def cofactor(m: Matrix):
        matrix_result = Matrix(m.row_dimension, m.column_dimension)
        for i in range(m.row_dimension):
            for j in range(m.column_dimension):
                subm = MatrixOperator.submatrix(m, i, j)
                cof = MatrixOperator.determinant(subm)
                if (i+j)%2==1:
                    cof = ComplexNumberOperator.negate(cof)
                matrix_result.set_element(i, j, cof)
        return matrix_result

    
    @staticmethod
    def determinant(m: Matrix):
        if m.row_dimension == m.column_dimension == 1:
            return m.get_element(0, 0)
        elif m.row_dimension == m.column_dimension == 2:
            return ComplexNumberOperator.subtract(
                    ComplexNumberOperator.multiply(m.get_element(0,0), m.get_element(1,1)),
                    ComplexNumberOperator.multiply(m.get_element(0,1), m.get_element(1,0)))
        elif m.row_dimension == m.column_dimension:
            det = ComplexNumber(ComplexNumberForm.Cartesian, 0, 0)
            for i in range(m.column_dimension):
                subm = MatrixOperator.submatrix(m, 0, i)
                cof = ComplexNumberOperator.multiply(m.get_element(0, i), MatrixOperator.determinant(subm))
                if i % 2 == 1:
                    cof = ComplexNumberOperator.negate(cof)
                det = ComplexNumberOperator.add(det, cof)
            return det
        return ComplexNumber(ComplexNumberForm.Invalid, 0, 0, "Determinant can be calculated ONLY in a square matrix")
    
    
    @staticmethod
    def submatrix(m: Matrix, r, c):
        matrix_result = Matrix(m.row_dimension - 1, m.column_dimension - 1)
        r_tmp = 0
        c_tmp = 0
        for i in range(m.row_dimension):
            if i == r:
                continue
            c_tmp = 0
            for j in range(m.column_dimension):
                if j == c:
                    continue
                matrix_result.set_element(
                    r_tmp, c_tmp, m.get_element(i, j)
                )
                c_tmp = c_tmp + 1
            r_tmp = r_tmp + 1
        return matrix_result