import math

from utils.winogradoriginal import winograd_original

def winograd_scaled(A, B, N, P, M):
    # Crear copias escaladas de A y B
    CopyA = [[0.0] * P for _ in range(N)]
    CopyB = [[0.0] * M for _ in range(P)]
    
    # Factores de escala
    a = norm_inf(A, N, P)
    b = norm_inf(B, P, M)
    lambda_val = math.floor(0.5 + math.log(b/a)/math.log(4))
    
    # Escalado
    multiply_with_scalar(A, CopyA, N, P, 2 ** lambda_val)
    multiply_with_scalar(B, CopyB, P, M, 2 ** (-lambda_val))
    
    # Usando Winograd con matrices escaladas
    return winograd_original(CopyA, CopyB, N, P, M)

def norm_inf(matrix, rows, cols):
    max_sum = float('-inf')
    for i in range(rows):
        row_sum = sum(abs(matrix[i][j]) for j in range(cols))
        max_sum = max(max_sum, row_sum)
    return max_sum

def multiply_with_scalar(A, CopyA, rows, cols, scalar):
    for i in range(rows):
        for j in range(cols):
            CopyA[i][j] = A[i][j] * scalar
