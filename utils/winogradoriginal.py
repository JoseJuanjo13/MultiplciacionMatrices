def winograd_original(A, B, N, P, M):
    result = [[0.0 for _ in range(N)] for _ in range(M)]
    upsilon = P % 2
    gamma = P - upsilon
    y = [0.0] * M
    z = [0.0] * N
    
    for i in range(M):
        aux = 0.0
        for j in range(0, gamma, 2):
            aux += A[i][j] * A[i][j+1]
        y[i] = aux
    
    for i in range(N):
        aux = 0.0
        for j in range(0, gamma, 2):
            aux += B[j][i] * B[j+1][i]
        z[i] = aux
    
    if upsilon == 1:
        # P is odd
        # The value A[i][P]*B[P][k] is missing in all auxiliary sums.
        PP = P - 1
        for i in range(M):
            for k in range(N):
                aux = 0.0
                for j in range(0, gamma, 2):
                    aux += (A[i][j] + B[j+1][k]) * (A[i][j+1] + B[j][k])
                result[i][k] = aux - y[i] - z[k] + A[i][PP] * B[PP][k]
    else:
        # P is even
        # The result can be computed with the auxiliary sums.
        for i in range(M):
            for k in range(N):
                aux = 0.0
                for j in range(0, gamma, 2):
                    aux += (A[i][j] + B[j+1][k]) * (A[i][j+1] + B[j][k])
                result[i][k] = aux - y[i] - z[k]
    
    return result
