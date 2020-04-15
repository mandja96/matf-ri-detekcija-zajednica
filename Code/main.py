import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

import GeneticOperation as GO
import LocalSearch
import buildGraph
import GirNew as GN

from sklearn.metrics.cluster import normalized_mutual_info_score


simulated_annealing = True
dataset_path = "./datasets/dolphins.txt"
nmi_benchmark = "dolphins" # dolphins / karate / jazz

# Normalized Mutual Information
def NMI(CommunityPartion, chromosome_length, MA):
    n = chromosome_length
    print(n)
    current_partition = [x for x in range(0, n)]
    # i - communities, 
    # j - vertices

    # [(0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 22), 
    # (8, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33)]
    for i in range(len(CommunityPartion)): 
        CommunityPartion[i] = list(CommunityPartion[i])
        print(CommunityPartion[i])
        for j in range(len(CommunityPartion[i])): 
            if MA:
                current_partition[CommunityPartion[i][j]] = i 
            else:
                current_partition[CommunityPartion[i][j]-1] = i 


    benchmark_karate = [0,0,0,0,0,0,0,0,1,1,
                        0,0,0,0,1,1,0,0,1,0,
                        1,0,1,1,1,1,1,1,1,1,
                        1,1,1,1]

    benchmark_dolphins = [1,0,1,1,1,0,0,0,1,0,
                          1,1,1,0,1,1,1,0,1,0,
                          1,1,0,1,1,0,0,0,1,1,
                          1,0,0,1,1,1,1,1,1,1,
                          1,0,1,1,1,1,1,1,0,1,
                          1,1,1,1,0,1,0,0,1,1,
                          0,1]
    
    benchmark = None
    if nmi_benchmark == "dolphins":
        benchmark = benchmark_dolphins
    elif nmi_benchmark == "karate":
        benchmark = benchmark_karate

    print('Partitions = ', current_partition)
    print('Number of communities: ', len(CommunityPartion))
    print('NMI:', normalized_mutual_info_score(benchmark, current_partition))

def MA():
    Gm = 1        #maximum numbers of generations
    Sp = 450      #populaton size
    Spool = Sp/2  #population of mating pool
    Stour = 2     #number of tournament
    Pc = 0.8      #crossover probability
    Pm = 0.2      #mutate probability
    Alpha = 0.2   #initial population parameter

    G=nx.Graph()
    K=nx.Graph()
    GN.load_graph(K, dataset_path)
    A = nx.adj_matrix(K)
    A = A.todense()
    buildGraph.buildGraph(G, A)

    # number of vertices
    chromosome_length = len(G.nodes())

    population=buildGraph.initPopulation(G, chromosome_length, Sp, Alpha) # initial population
    t = 0     # generation numbers
    BestPop = np.zeros([Gm, chromosome_length]) # for each generation one best
    while t < Gm:
        parents = GO.selection(population, A, Spool, Stour)
        children=GO.CrossoverMutate(G, parents, Pc, Pm)

        CurrChild = LocalSearch.FindBest(children, A)
        Bestchild = CurrChild 

        if not simulated_annealing:
            IsLocal = False
            while not IsLocal:
                L = LocalSearch.FindNeighbors(Bestchild)

                best = LocalSearch.FindBest(L,A)
                if GO.fitness(A,best) > GO.fitness(A,Bestchild):
                    Bestchild = best
                else:
                    IsLocal = True
        else:
            i = 1 
            while i < 500:
                L = LocalSearch.FindNeighbors(CurrChild)
                NewChild = random.randint(0, len(L)-1)
                # NewChild = LocalSearch.FindBest(L, A)
                if GO.fitness(A, L[NewChild]) > GO.fitness(A, CurrChild):
                # if GO.fitness(A, NewChild) > GO.fitness(A, CurrChild):
                    CurrChild = L[NewChild]
                    # CurrChild=NewChild
                else:
                    p = 1.0 / i ** 0.5
                    q = random.uniform(0, 1)
                    if p > q:
                        CurrChild = L[NewChild]
                        # CurrChild=NewChild
                if GO.fitness(A, L[NewChild]) > GO.fitness(A, Bestchild):
                # if GO.fitness(A, NewChild) > GO.fitness(A, Bestchild):
                    Bestchild = L[NewChild]
                    # Bestchild=NewChild            
                i += 1

        population = buildGraph.updatePopulation(population, A, children, Bestchild)
        print('Generation is ', t+1)
        print('Max fitness = ', GO.fitness(A, population[0]))
        print(LocalSearch.GetCommunity(population[0]))
        BestPop[t] = population[0]
        t += 1

    FinalResult = LocalSearch.FindBest(BestPop, A)
    CommunityPartion = LocalSearch.GetCommunity(FinalResult)
    print('Community partition: ', CommunityPartion)
    return CommunityPartion, chromosome_length

def plot_graph(CommunityPartion, MA):
    # Plot the graph
    node_color = {}
    colors = ['green', 'red', 'blue', 'orange', 'yellow', 'magenta', 'purple', 'cyan']
    for i in range(len(CommunityPartion)):
        community = list(CommunityPartion[i])
        for node in community:
            node_color[node] = colors[i]

    graph = nx.Graph()
    GN.load_graph(graph, dataset_path)       
    tmp = []
    nodes = graph.nodes()
    for node in nodes:
        if MA:
            tmp.append(node_color[node-1]) 
        else:
            tmp.append(node_color[node]) 


    pos = nx.spring_layout(graph)
    nx.draw(graph, node_color=tmp, pos=pos, with_labels=True, font_color='white', alpha=0.7)
    plt.show()

def gn(chromosome_length):
    graph = nx.Graph()
    GN.load_graph(graph, dataset_path)
    n = graph.number_of_nodes()
    A_girvan = nx.adj_matrix(graph)
    m_ = 0.0
    for i in range(n):
        for j in range(n):
            m_ += A_girvan[i, j]
    m_ = m_ / 2.0
    Orig_deg = {}
    Orig_deg = GN.UpdateDeg(A_girvan, graph.nodes())
    girvan_best = GN.GirvanNewman(graph, A_girvan, Orig_deg, m_)
    NMI(girvan_best, chromosome_length, MA=False)
    plot_graph(girvan_best, MA=False)

if __name__ == '__main__':
    CommunityPartion, chromosome_length = MA()
    plot_graph(CommunityPartion, MA=True)
    NMI(CommunityPartion, chromosome_length, MA=True)
    print("--------------------------------------------")
    gn(chromosome_length)