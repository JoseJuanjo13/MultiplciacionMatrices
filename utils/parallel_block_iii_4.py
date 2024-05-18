import numpy as np
from concurrent.futures import ThreadPoolExecutor

def block_multiply(A, B, C, i1, j1, k1, size, bsize):
    # Procesamiento del bloque de la matriz
    for i in range(i1, min(i1 + bsize, size)):
        for j in range(j1, min(j1 + bsize, size)):
            for k in range(k1, min(k1 + bsize, size)):
                C[i, j] += A[i, k] * B[k, j]

def parallel_block_iii_4(A, B, size, bsize=64):
    A = np.array(A, dtype=np.int64) if not isinstance(A, np.ndarray) else A
    B = np.array(B, dtype=np.int64) if not isinstance(B, np.ndarray) else B
    C = np.zeros((size, size), dtype=np.int64)

    with ThreadPoolExecutor() as executor:
        futures = []
        for i1 in range(0, size, bsize):
            for j1 in range(0, size, bsize):
                for k1 in range(0, size, bsize):
                    futures.append(executor.submit(block_multiply, A, B, C, i1, j1, k1, size, bsize))
        for future in futures:
            future.result()
    return C