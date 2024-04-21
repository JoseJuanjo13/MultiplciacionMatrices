import numpy as np
from concurrent.futures import ProcessPoolExecutor

def optimal_block_size(size, max_block_size=64):
    # Encuentra el mayor divisor de 'size' que sea menor o igual a max_block_size
    for bsize in range(max_block_size, 0, -1):
        if size % bsize == 0:
            return bsize
    return 1  # En caso extremo donde no se encuentra divisor adecuado, usa 1

def block_multiply(i1, j1, k1, size, bsize, A, B, C):
    for i in range(i1, min(i1 + bsize, size)):
        for j in range(j1, min(j1 + bsize, size)):
            for k in range(k1, min(k1 + bsize, size)):
                C[i, k] += A[i, j] * B[j, k]
    return (i1, j1, k1, C[i1:i1+bsize, k1:k1+bsize])

def parallel_block_iv4(A, B, size):
    bsize = optimal_block_size(size)  # Calcula el tamaño de bloque óptimo

    A = np.array(A, dtype=np.int64)  # Convierte A a int64
    B = np.array(B, dtype=np.int64)  # Convierte B a int64
    A_result = np.zeros((size, size), dtype=np.int64)  # Crea A_result como int64

    with ProcessPoolExecutor() as executor:
        futures = []
        for i1 in range(0, size, bsize):
            for j1 in range(0, size, bsize):
                for k1 in range(0, size, bsize):
                    futures.append(executor.submit(block_multiply, i1, j1, k1, size, bsize, A, B, A_result))

        for future in futures:
            i1, j1, k1, partial_result = future.result()
            # Actualiza A_result con el resultado parcial
            A_result[i1:i1+bsize, k1:k1+bsize] += partial_result

    return A_result