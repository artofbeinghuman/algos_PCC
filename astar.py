# ----------------------------------------------------------------
#
#                       Algorithme Astar   1.0
#   -> Je n'ai pas encore testé sur les graphes du prof
# Si vous avez des idées d'optimisation c'est tout benef.
# ----------------------------------------------------------------
infty = 10**15

def search_first(L,e):
    """ Algorithme de recherche par dichotomie selon la première composante """
    a = 0
    b = len(L)
    while b-a > 1:
        c = (a+b)//2
        if L[c][0] > e[0]:
            b = c-1
        elif L[c][0] < e[0]:
            a = c
        else:
            return a
    return a

def get(d,cle):
    return d[cle]

class File:
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
            (self.l[index],self.l[index//2]) = (self.l[index//2],self.l[index])
            return self.upper_propagation(index//2)
        else:
            return index
        
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
        """ Récupère l'élément de plus grande priorité : O(log n) """
        e = self.l[0]
        self.l[0] = (self.l[0][0],infty)
        new_index = self.upper_propagation(len(self.l)-1)
        del self.l[-1]
        self.d[e[0]] = new_index
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
    return 0 #Ici je suppose qu'il n'y a pas de cycle négatif

def w(u,v):
    return p[u,v]

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
        u = F.pop()[0]
        T.append(u)
        if u == g:
            return (d,P)
        for v in G[u]:
            cst = d[u] + w(u,v)
            if F.contains(v):
                if d[v] > cst:
                    d[v] = cst
                    P[v] = u
                    print("modify",v,cle(v))
                    F.modify(v,cle(v))
            elif v in T:
                if d[v] > cst:
                    d[v] = csr
                    P[v] = u
                    print("add",v,cle(v))
                    F.add((v,cle(v)))
            else:
                d[v] = cst
                P[v] = u
                print("add",v,cle(v))
                F.add((v,cle(v)))
    return False

#Definition du graphe
G = [[1,3],[2],[3],[]]
#Definition des poids des aretes
p = {}
p[0,1] = 0.1
p[0,3] = 10
p[1,2] = 0.01
p[2,3] = 0.01
print(Astar(G,0,2))
