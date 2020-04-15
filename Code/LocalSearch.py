import GeneticOperation as GO
import numpy as np
import copy

def GetCommunity(chromosome):
    L = []
    cluster = ()
    for i in range(len(chromosome)):
        V = ()
        ider = chromosome[i]
        if ider in cluster:
            continue
        else:
            cluster += (ider,)
            V += (i,)
        for j in range(i+1, len(chromosome)):
            if chromosome[j]==ider:
                V +=(j,)
        L.append(V)
    return L

def FindNeighbors(chromosome):
    # L = [(1,3,5),(2,4,6)]
    # nodes indexes

    L = GetCommunity(chromosome)
    m = len(L)
    n = 0
    for i in range(m):
        n +=len(L[i])

    # change one gene once, others stays the same
    # 0, 0, 0 -> 1, 0, 0 -> 0, 1, 0 -> 0, 0, 1
    # or
    # 1, 1, 1 -> 2, 1, 1 -> 1, 2, 1 -> 1, 1, 2 ...
    if m == 1:
        # print("m == 1")
        neighbors=np.empty([n,n])
        for k in range(len(L[0])):
            for j in range(len(L[0])):
                if k == j:
                    if L[0][k]+1 > n-1:
                        neighbors[k][j] = L[0][k]-1
                    else:
                        neighbors[k][j] = L[0][k]+1 
                else:
                    neighbors[k][j] = L[0][k] 
    else:
        neighbors=np.empty([n*(m-1), n])
        num = 0
        for i in range(m):
            for k in range(len(L[i])):

                for j in range(m):
                    if i==j:
                        continue
                    else:
                        neighbors[num] = copy.deepcopy(chromosome)
                        neighbors[num][L[i][k]] = chromosome[L[j][0]]
                        num +=1
    return neighbors

def FindBest(P, A):
    best = 0
    for i in range(len(P)):
        if GO.fitness(A,P[i]) > GO.fitness(A,P[best]):
            best = i
    return P[best]
