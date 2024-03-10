import numpy as np

def generate_random_matrix(n):
    return np.random.randint(100000, size=(n, n)).tolist()

def matrix_multiply_iterative(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación.")

    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    return result