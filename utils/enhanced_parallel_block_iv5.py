import numpy as np
from concurrent.futures import ProcessPoolExecutor

def matrix_block_multiply(A, B, C, start, end, size, bsize):
    for i1 in range(start, end, bsize):
        for j1 in range(0, size, bsize):
            for k1 in range(0, size, bsize):
                for i in range(i1, min(i1 + bsize, size)):
                    for j in range(j1, min(j1 + bsize, size)):
                        for k in range(k1, min(k1 + bsize, size)):
                            C[i, k] += A[i, j] * B[j, k]  # Usando indexación de NumPy
    return C

def enhanced_parallel_block_iv5(A, B, size, bsize=64):
    A = np.array(A, dtype=np.int64)
    B = np.array(B, dtype=np.int64)
    C = np.zeros((size, size), dtype=np.int64)

    half_size = size // 2

    with ProcessPoolExecutor() as executor:
        future1 = executor.submit(matrix_block_multiply, A, B, C, 0, half_size, size, bsize)
        future2 = executor.submit(matrix_block_multiply, A, B, C, half_size, size, size, bsize)

        # Esperar a que ambas partes completen
        part1 = future1.result()
        part2 = future2.result()

        # No es necesario sumar las partes porque C es compartido
    return C