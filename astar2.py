# ----------------------------------------------------------------
#
#                       Algorithme Astar   1.0
#   -> Je n'ai pas encore testé sur les graphes du prof
# Si vous avez des idées d'optimisation c'est tout benef.
# ----------------------------------------------------------------


infty = 10**15

from importgraph import *
import copy

def search(L,e,comp):
    """ Algorithme de recherche par dichotomie selon la première composante """
    i = 0
    while i <= len(L)-1 and L[i][comp] < e[comp]:
            i += 1
    return i

def get(d,cle):
    return d[cle]

class File:
    l = None #De la forme [priority,key],...

    def __init__(self):
        self.l = []

    def __repr__(self):
        return str(self.l)
        
    def add(self,e):
        """ Ajoute un élément dans la file : O(log n) """
        index = search(self.l,e,0)
        self.l.insert(index,e)

    def modify(self,val,cle):
        """ Modifie la clé d'une entrée en O(n)"""
        index = -1
        for i in range(len(self.l)):
            if self.l[i][1] == cle:
                index = i
        if index == -1:
            assert False #Not in the list
        del self.l[index]
        e2 = (val,cle)
        index2 = search(self.l,e2,0)
        self.l.insert(index2,e2)

    def pop(self):
        """ Récupère l'élément de plus grande priorité : O(1) """
        r = self.l[0]
        del self.l[0]
        return r

    def empty(self):
        """ Test si la file est vide : O(1) """
        return self.l == []

    def contains(self,v):
        """ Test si la file contient un élément : O(n) """
        for (p,k) in self.l:
            if k == v:
                return True
        return False
        

class File2:
    """ Implémente une file (pile fifo) -> utiliser un tas"""
    l = None #Les entrées sont sous la forme : (priorité,val)
    d = None #Un dictionnaire des emplacements des éléments dans l

    def __repr__(self):
        """ Sert a afficher self.l quand on fait print(file)"""
        return str(self.l)
    
    def __init__(self):
        self.l = []
        self.d = {}

    def upper_propagation(self,index):
        """ Reforme un tas en remontant à partir de l'index : O(log n)"""
        if self.l[index][1] < self.l[index//2][1]:
            (cle1,v1) = self.l[index]
            (cle2,v2) = self.l[index//2]
            self.d[cle1] = index//2
            self.d[cle2] = index
            (self.l[index],self.l[index//2]) = copy.copy((self.l[index//2],self.l[index]))
            return self.upper_propagation(index//2)
        else:
            return index

    def force_upper_propagation(self,index):
        while index != 0:
            index = self.upper_propagation(index)//2
        return 0
        
    def add(self,e):
        """ Ajoute un élément dans la file : O(log n) """
        self.l.append(e)
        index = self.upper_propagation(len(self.l)-1)
        self.d[e[0]] = index

    def modify(self,cle,v):
        """ Modifie la clé d'une entrée en O(log n)"""
        index = self.d[cle]
        self.l[index] = (self.l[index][0],v)
        new_index = self.upper_propagation(index)

    def pop(self):
        """ Récupère l'élément de plus grande priorité : O(log² n) """
        e = self.l[0]
        self.l[0] = (e[0],infty)
        while self.d[e[0]] != len(self.l)-1:
            new_index = self.force_upper_propagation(len(self.l)-1)
        del self.l[-1]
        return e

    def empty(self):
        """ Test si la file est vide : O(1) """
        return self.l == []

    def contains(self,v):
        """ Test si la file contient un élément : O(1) """
        try:
            get(self.d,v)  #Il peut valoir 0 aussi
            return True
        except KeyError:
            return False

def h(x): #Difficile de donner de bonnes heuristiques sans hypothèses sur les graphes
    """ Comme A* est surtout utilisé pour le path finding dans le plan, on utilise souvent :
pour a=(x,y) et b=(x2,y2) -> ha(b) = ((x-x2)**2 + (y-y2)**2)**0.5 mais ici on n'a pas
l'hypothèse que l'on travail sur le plan. J'avais aussi pensé à utiliser l'hypothèse que le
graphe respecte l'inégalité triangulaire afin d'utiliser la même fonction à un coefficient
multiplicatif près qui pourrait être la valeur du plus petit arc strictement positif (en
supposant qu'il n'y a pas d'arc négatifs"""
    return 0 #Ici je suppose qu'il n'y a pas de cycle négatif (sinon il faut mettre -infini)

# Il faut renseigner h en global !!!
def Astar(G,s,g):
    def cle(u):
        return d[u] + h(u)
    """ Algorithme Astar """
    P = [None]*len(G)
    d = [0]*len(G)
    B = [False]*len(G)
    F = File() #File de priorité
    F.add((s,cle(s)))
    T = []
    while not(F.empty()):
        u = F.pop()[1]
        #print(F)
        T.append(u)
        if u == g:
            return (d,P)
        for (v,w) in G[u]:
            #print(u,v)
            #print(u,v,w)
            cst = d[u] + w
            if F.contains(v):
                if d[v] > cst:
                    d[v] = cst
                    P[v] = u
                    #print("modif")
                    #print("modify",cle(v),v)
                    F.modify(cle(v),v)
            elif v in T:
                if d[v] > cst:
                    d[v] = cst
                    P[v] = u
                    #print("add")
                    #print("add",cle(v),v)
                    F.add((cle(v),v))
            else:
                d[v] = cst
                P[v] = u
                #print("add")
                #print("add",cle(v),v)
                F.add((cle(v),v))
    return (False,None)

def get_predecessor(P,s,u):
    l = [u]
    while s != u:
        l.append(P[u])
        u = P[u]
    return l

def test():
    import bellman as bm
    #Definition du graphe
    G = import_graph("graphs\CachanGraphe5.txt")
    #print(G[0])
    for i in range(1,1500):
        (bfb,bfd,bfPi) = bm.BellmanFord(G,0)
        ast = Astar(G,0,i)
        ras = ast[0][i]
        rbf = bfd[i]
        #print(ast[0][0::10])
        if rbf != ras:
            print("Error : "+str(i)+" "+str(ras)+" "+str(rbf))
        print(get_predecessor(ast[1],0,i),get_predecessor(bfPi,0,i))
            
