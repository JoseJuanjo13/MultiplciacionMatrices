def naiv_on_array(A, B, N, P, M):
    result = [[0.0 for _ in range(M)] for _ in range(N)]
    
    for i in range(N):
        for j in range(M):
            for k in range(P):
                result[i][j] += A[i][k] * B[k][j]

    return result