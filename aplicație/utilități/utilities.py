# functie care returneaza minorul unei matrice(?)
def matrix_minor(matrix, order, row, column):

    result_matrix = []
    for i in range(order):
        add_row = []
        for j in range(order):
            if i == row or j == column:
                continue
            else:
                add_row.append(matrix[i][j])
        if i == 0:
            pass
        else:
            result_matrix.append(add_row)

    return result_matrix

# functie care returneaza determinantul de ordin 2
def second_order_det(matrix):

    i = 0
    j = 0
    return (matrix[i][j] * matrix[i+1][j+1]) - (matrix[i][j+1] * matrix[i + 1][j])

# functie care returneaza determinantul de ordin 3
def third_order_det(matrix):

    sum_of_determinant = 0
    for i in range(1):
        for j in range(3):
            minor_of_det = matrix_minor(matrix, 3, i, j)
            sign = pow(-1, i + j + 2)
            result = matrix[i][j] * sign * second_order_det(minor_of_det)
            sum_of_determinant += result
    return sum_of_determinant

