import numpy as np

def sequential_block_v3(A, B, size, bsize=64):
    # Convertir A y B a arrays de NumPy si no lo son
    if isinstance(A, list):
        A = np.array(A, dtype=np.int64)
    if isinstance(B, list):
        B = np.array(B, dtype=np.int64)
    C = np.zeros((size, size), dtype=np.int64)
    
    for i1 in range(0, size, bsize):
        for j1 in range(0, size, bsize):
            for k1 in range(0, size, bsize):
                for i in range(i1, min(i1 + bsize, size)):
                    for j in range(j1, min(j1 + bsize, size)):
                        for k in range(k1, min(k1 + bsize, size)):
                            C[k, i] += A[k, j] * B[j, i]
    return C