import math

def strassen_winograd(A, B, N, P, M):
    MaxSize = max(N, P, M)
    if MaxSize < 16:
        MaxSize = 16  # otherwise it is not possible to compute k
    k = math.floor(math.log(MaxSize) / math.log(2)) - 4
    m = math.floor(MaxSize * pow(2, -k)) + 1
    NewSize = m * pow(2, k)
    
    # add zero rows and columns to use Strassen's algorithm
    NewA = [[0.0] * NewSize for _ in range(NewSize)]
    NewB = [[0.0] * NewSize for _ in range(NewSize)]
    AuxResult = [[0.0] * NewSize for _ in range(NewSize)]
    
    for i in range(N):
        for j in range(P):
            NewA[i][j] = A[i][j]
    
    for i in range(P):
        for j in range(M):
            NewB[i][j] = B[i][j]
    
    strassen_winograd_step(NewA, NewB, AuxResult, NewSize, m)
    
    # extract the result
    Result = [[0.0] * M for _ in range(N)]
    for i in range(N):
        for j in range(M):
            Result[i][j] = AuxResult[i][j]
    
    return Result

def strassen_winograd_step(A, B, Result, size, m):
    # Your Strassen-Winograd algorithm implementation for the step here
    pass
