# utils/enhanced_parallel_block.py
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def enhanced_parallel_block(A, B, size, bsize):
    A = np.array(A, dtype=np.int64)
    B = np.array(B, dtype=np.int64)
    C = np.zeros((size, size), dtype=np.int64)

    def process_block(start, end):
        for i1 in range(start, end, bsize):
            for j1 in range(0, size, bsize):
                for k1 in range(0, size, bsize):
                    for i in range(i1, min(i1 + bsize, size)):
                        for j in range(j1, min(j1 + bsize, size)):
                            for k in range(k1, min(k1 + bsize, size)):
                                C[i][j] += A[i][k] * B[k][j]

    with ThreadPoolExecutor() as executor:
        executor.submit(process_block, 0, size // 2)
        executor.submit(process_block, size // 2, size)
    
    return C.tolist()