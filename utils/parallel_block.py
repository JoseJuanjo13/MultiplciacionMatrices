# utils/parallel_block.py
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def parallel_block(A, B, size, bsize):
    A = np.array(A, dtype=np.int64)  # Asegurarse de que A y B son de tipo int64
    B = np.array(B, dtype=np.int64)
    C = np.zeros((size, size), dtype=np.int64)  # Usar int64 para evitar overflow
    
    def process_block(i1, j1, k1):
        for i in range(i1, min(i1 + bsize, size)):
            for j in range(j1, min(j1 + bsize, size)):
                for k in range(k1, min(k1 + bsize, size)):
                    C[i][j] += A[i][k] * B[k][j]

    with ThreadPoolExecutor() as executor:
        for i1 in range(0, size, bsize):
            for j1 in range(0, size, bsize):
                for k1 in range(0, size, bsize):
                    executor.submit(process_block, i1, j1, k1)
    
    return C.tolist()  # Convertir el resultado final de nuevo a lista si es necesario
