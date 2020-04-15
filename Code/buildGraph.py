import random
import numpy as np
import GeneticOperation as GO

def buildGraph(G, adj_matrix):
    row,column=adj_matrix.shape
    for i in range(row):
        for j in range(column):
            if adj_matrix[i, j] > 0:
                G.add_edge(i, j)

# n = number of vertices
# pop = population with chromosomes
def initPopulation(G, n, pop, Alpha): 
    x = np.zeros([pop, n])
    for i in range(pop):
        x[i] = range(1, n+1)
    for i in range(pop):
        t = 0
        while t <= n * Alpha:
            r = random.randint(1, n)
            if r in G.nodes():
                ider = x[i][r-1]
                neighbors = G.edges(r)
                for j in range(len(neighbors)):
                    neighbor = list(neighbors)[j][1]
                    x[i][neighbor-1] = ider
                t += 1
    return x

def updatePopulation(P, A, children, best):
    row, column = P.shape
    P_new = np.zeros([row, column])

    # len(best) je (34,) to je jednodimenziono, znaci treba + 1
    AllP = np.zeros([row+len(children)+1,column])
    AllP[0:row] = P
    AllP[row:row+len(children)] = children
    AllP[-1] = best
    
    L = np.zeros([1,len(AllP)])
    for i in range(len(AllP)):
        L[0][i] = GO.fitness(A,AllP[i])
    S = np.argsort(L[0])
    t =-1    
    for i in range(len(P_new)):
        P_new[i] = AllP[S[t]]
        t-=1
    return P_new

