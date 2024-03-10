def naive_loop_unrolling_two(A, B, N, P, M):
    result = [[0.0 for _ in range(M)] for _ in range(N)]
    
    if P % 2 == 0:
        for i in range(N):
            for j in range(M):
                aux = 0.0
                for k in range(0, P, 2):
                    aux += A[i][k] * B[k][j] + A[i][k + 1] * B[k + 1][j]
                result[i][j] = aux
    else:
        PP = P - 1
        for i in range(N):
            for j in range(M):
                aux = 0.0
                for k in range(0, PP, 2):
                    aux += A[i][k] * B[k][j] + A[i][k + 1] * B[k + 1][j]
                result[i][j] = aux + A[i][PP] * B[PP][j]
    
    return result
