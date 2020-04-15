import numpy as np
import LocalSearch
import random

# 0.5 is default density
# smaller than that detects smaller communities
density_lambda = 0.8

def selection(P, A, pool, tour):
    row,column = P.shape
    pool = int(pool)
    
    parents = np.zeros([pool, column])
    for i in range(pool):
        a = random.randint(0, row-1)
        for j in range(tour):
            b = random.randint(0, row-1)
            if fitness(A,P[a]) < fitness(A,P[b]):
                best = b
            else:
                best = a
        parents[i] = P[best]  
    return parents

def CrossoverMutate(G, parents, pc, pm):
    row,column = parents.shape
    for i in range(0, row-1, 2):
        r = random.random()
        if r < pc:
            R1 = random.randint(0, column-1)
            c = parents[i].copy()
            cluster1 = parents[i+1][R1]
            for j in range(0, column-1):
                if parents[i+1][j] == cluster1:
                    parents[i][j] = cluster1
            R2=random.randint(0, column-1)
            cluster2 = c[R2]
            for j in range(0, column-1):
                if c[j] == cluster2:
                    parents[i+1][j] = cluster2
        rr = random.random()
        #mutate operation
        if rr < pm:  
            r1 = random.randint(0, row - 1)
            for i in range(column):
                r2 = random.randint(0, column - 1)
                neighbors = G.edges(r2)
                r3 = random.randint(0, len(neighbors) - 1)
                neighbor = list(neighbors)[r3][1]
                parents[r1][r2] = parents[r1][neighbor]
    return parents

def fitness(A,x):
    # degrees of nodes
    bw = A.sum(axis=1)
    L = LocalSearch.GetCommunity(x)
    
    mod = 0.0
    for i in range(len(L)):
        com = 0.0
        cut = 0.0
        for j in range(len(L[i])):
            com1 = 0.0
            for m in range(len(L[i])):
                com1 += A[L[i][j], L[i][m]]
            com += com1
            cut += (bw[L[i][j]] - com1)
        mod += (2*density_lambda*com-2*(1-density_lambda)*cut)/len(L[i])
    return mod