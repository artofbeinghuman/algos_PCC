import numpy as np
from fibonacci import Fibo as File

def dijkstra(G,s):
    P = [None for i in range(len(G))]
    d = [np.infty for i in range(len(G))]
    d[s] = 0
    F = File()
    F.initialize(len(G)) #Initialisation (voir le fichier contenant les tas de fibonacci)
    while not F.empty():
        u = F.pop()
        #Parcours des successeurs
        for (v,w) in G[u]:
            if d[v] > d[u] + w:
                #Mise a jour de v
                d[v] = d[u] + w
                P[v] = u
                F.modify(d[v],v)
    return d,P
