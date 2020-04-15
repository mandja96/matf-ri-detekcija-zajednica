import matplotlib.pyplot as plt
import random
import networkx

# 0.5 is default density
# smaller than that detects smaller communities
density_lambda = 0.3

# dolphins = 62
# karate = 34
def load_graph(graph, input_file):
    graph.add_nodes_from([x for x in range(1, 63)])
    # u, v
    # u, v, w
    with open(input_file) as f:
        lines = f.read().splitlines()
        for line in lines:
            values = line.split(' ')
            # values = [x for x in values if x != ''] # ovo je za Jazz 
            if len(values) == 3:
                graph.add_edge(int(values[0]), 
                               int(values[1]), 
                               weight = float(values[2]))
            else:
                graph.add_edge(int(values[0]),
                               int(values[1]),
                               weight = 1.0)
def GNStep(G):
    init_ncomp = networkx.number_connected_components(G)
    ncomp = init_ncomp

    while ncomp <= init_ncomp:
        bw = networkx.edge_betweenness_centrality(G, weight='weight')
        max_ = max(bw.values())
        # remove all of them
        for k,v in bw.items():
            if float(v) == max_:
                G.remove_edge(k[0], k[1])
        ncomp = networkx.number_connected_components(G)

def GNGetDensityModularity(G, A, L):
    A = A.todense()
    bw = A.sum(axis=1)
    mod = 0.0
    for i in range(len(L)):
        com = 0.0
        cut = 0.0
        L[i] = list(L[i])
        for j in range(len(L[i])):
            com1 = 0.0
            for m in range(len(L[i])):
                com1 +=A[L[i][j]-1,L[i][m]-1]
            com += com1
            cut += (bw[L[i][j]-1]-com1)
        mod += (2*density_lambda*com-2*(1-density_lambda)*cut)/len(L[i])
    return mod

def GNGetModularity(G, deg_, m_):
    New_A = networkx.adj_matrix(G)
    New_deg = {}
    New_deg = UpdateDeg(New_A, G.nodes())

    comps = networkx.connected_components(G)
    print("Current number of communities: ", networkx.number_connected_components(G))

    # basic modularity
    Mod = 0
    for c in comps:
        edges_in_comm = 0
        random_edges = 0
        for u in c:
            edges_in_comm += New_deg[u]
            random_edges += deg_[u]
        Mod += (float(edges_in_comm - float(random_edges*random_edges)/float(2*m_)))
    Mod = Mod/float(2*m_)

    print("Modularity: ", Mod)
    return Mod

def UpdateDeg(A, nodes):
    deg_dict = {}
    n = len(nodes)
    B = A.sum(axis=1)
    i = 0
    for node_id in list(nodes):
        deg_dict[node_id] = B[i, 0]
        i += 1
    return deg_dict


def GirvanNewman(G, A, Orig_deg, m_):
    BestQ = 0.0
    Q = 0.0
    while True:
        GNStep(G)
        Q = GNGetModularity(G, Orig_deg, m_)
        Q = GNGetDensityModularity(G, A, list(networkx.connected_components(G)))
        print("Modularity of decomposed G: ", Q)
        if Q>BestQ:
            BestQ = Q
            Bestcomps = list(networkx.connected_components(G))
            print("Components: ", Bestcomps)
        if G.number_of_edges() == 0:
            break

        if BestQ > 0.0:
            print("Max modularity (Q): ", BestQ)
            print("Graph communities: ", Bestcomps)
            print("Number of communities: ", len(Bestcomps))
        else:
            print("Max modularity (Q): ", BestQ)
    return Bestcomps

# def main():
#     G = networkx.Graph()
#     load_graph(G, "./karate.txt")

#     # val_map = {'A': 1.0,
#     #            'D': 0.5714285714285714,
#     #            'H': 0.0}

#     # values = [val_map.get(node, 0.25) for node in G.nodes()]

#     networkx.draw(G, with_labels = True, font_color='white')
#     plt.show()
    
#     n = G.number_of_nodes()
#     print("Number of nodes = {}.".format(n))

#     A = networkx.adj_matrix(G)
#     # print(adj_matrix)

#     m_ = 0.0
#     for i in range(n):
#         for j in range(n):
#             m_ += A[i, j]
#     m_ = m_ / 2.0
#     print("Init modularity = {}.".format(m_))

#     Orig_deg = {}
#     Orig_deg = UpdateDeg(A, G.nodes())

#     GirvanNewman(G, A, Orig_deg, m_)

# if __name__ == '__main__':
#     main()

