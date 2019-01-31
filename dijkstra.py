import numpy as np
#from astar2 import File
from astar2 import Astar
from parcours import tas as File

def Dijkstra(G,s):
    #Algorithme de Dijkstra avec des tas classique (on n'a pas reussit a faire
    #les tas de Fibonacci car python ne permet pas de faire des pointeurs
    #facilement -> Implémentation très difficile (le code qui a été testé pour
    #les implémenté est dans le dossier github)
    P = [None for i in range(len(G))]
    d = [np.infty for i in range(len(G))]
    d[s] = 0
    F = File()
    l = [(np.infty,i) for i in range(len(G))]
    l[s]= (s,0)
    for i in l:
        F.add(i) #Initialisation (voir le fichier contenant les tas de fibonacci)
    while not F.empty():
        #print(F.pop())
        u = F.pop()
        #Parcours des successeurs
        for (v,w) in G[u]:
            if d[v] > d[u] + w:
                #Mise a jour de v
                d[v] = d[u] + w
                P[v] = u
                F.modify(d[v],v)
    return d,P

"""from importgraph import import_graph
g, index_to_vertex_name = import_graph("graphs/CachanGraphe7.txt", True)
#g = [[(1,0.2),(2,0.7)],[(2,0.4)],[(4,0.2),(5,0.8)],[],[],[]]
(d,P) = Dijkstra(g,0)
for t in range(100):
    (dstar,Pstar) = Astar(g,0,t)
    print(dstar[t],d[t])
    if dstar[t] == d[t]:
        print("pass",t)
    else:
        print("Error : ",t,dstar[t],d[t])
"""
