import sys
sys.setrecursionlimit(int(10e7))
#Représentation des graphes: listes d'adjacence
grap = [[2,1,5],
[2],[3],[4,9],[1,8],[],[5],[],[12],[10],[11],[],[]]


##Parcours de graphes

def aff(s):
    """fonction d'affichage"""
    print("on explore "+str(s)+"!")
    
def finaff(s):
    """fonction d'affichage"""
    print(str(s)+"\test fini")
    
def plarg(G, s0, inconnu=None, f=aff):
    """parcours en largeur (préfixe): G un graphe, s0 un sommet de G, f une fonction"""
    n = len(G)
    if inconnu == None:#initialisation de inconnu
        inconnu = [True for _ in range(n)]
    F = [s0]
    while F != []:
        s = F.pop()
        if inconnu[s] :
            f(s)
            inconnu[s] = False
            F = G[s] + F#ajoute tous les voisins
    #ici on a effectué le parcours largeur depuis s0 dans G

def plcomp(G,f=aff):
    """parcours en largeur complet (préfixe): G un graphe, f une fonction exécutée sur chaque sommet"""
    inconnu = [True for _ in range(len(G))]
    for i in range(len(G)):
        plarg(G,i,inconnu,f)

def pprof(G, s0, inconnu=None, f= aff, g=finaff):
    """parcours en profondeur (préfixe): G un graphe, s0 un sommet"""
    n = len(G)
    if inconnu == None:
        inconnu = [True for _ in range(n)]
    
    def prec(G,s0):
        f(s0)
        for s in G[s0]:
            if inconnu[s]:
                inconnu[s] = False
                prec(G,s)
        g(s0)
    prec(G,s0)

def ppcomp(G,f=aff,g=finaff):
    """ parcours en profondeur complet: 
    G : un graphe (orienté ou non)
    f : fonction exécutée avant le parcours des fils d'un sommet
    g : fonction exécutée après le parcours des fils d'un sommet"""
    inconnu = [True for _ in range(len(G))]
    for i in range(len(G)):
        if inconnu[i]:
            pprof(G,i,inconnu,f,g)

def pptime(G,ordre_enum=None):
    """ parcours en profondeur complet, avec indications de temps:
    G : un graphe (orienté ou non)
    ordre_enum: ordre d'énumération des sommets"""
    if ordre_enum == None:
        ordre_enum = list(range(len(G)))
    inconnu = [True for _ in range(len(G))]
    deb = [-1 for _ in range(len(G))]
    fin = [-2 for _ in range(len(G))]
    time = 0
    def prec(G,s0,time):
        time += 1
        deb[s0] = time
        for s in G[s0]:
            if inconnu[s]:
                inconnu[s] = False
                time = prec(G,s,time)
        time += 1
        fin[s0] = time
        return time
    for i in ordre_enum:
        if inconnu[i]:
            time = prec(G,i,time)
    return deb,fin

    
def pp_arbres_parcours(G,ordre_enum=None):
    """ parcours en profondeur complet, avec indications de temps:
    G : un graphe (orienté ou non)
    ordre_enum: ordre d'énumération des sommets"""
    if ordre_enum == None:
        ordre_enum = list(range(len(G)))
    inconnu = [True for _ in range(len(G))]
    cfc = 0
    arbres = [(-1) for _ in range(len(G))]
    def prec(G,s0,arbres):
        arbres[s0] = cfc
        for s in G[s0]:
            if inconnu[s]:
                inconnu[s] = False
                arbres = prec(G,s,arbres)
        return arbres
    for i in ordre_enum:
        if inconnu[i]:
            cfc += 1
            arbres = prec(G,i,arbres)
    return arbres
##Applications du parcours en profondeur

def cfcno(G):#algorithme pour graphes non orientés
    n = len(G)
    couleur = 0
    couleurs = [(-1) for _ in range(n)]
    inconnu = [True for _ in range(n)]
    def colorie(s):
        couleurs[s] = couleur
    for i in range(n):
        if inconnu[i]:
            couleur += 1
            pprof(G,i,inconnu,colorie)
    return couleurs


def transpose_grp(G):
    """transpose le graphe G: en temps linéaire O(S+A)"""
    n = len(G)
    Gt = [[] for i in range(n)]
    for s in range(n):#O(S)
        for t in G[s]:#O(deg(s))
            Gt[t].append(s)
    return Gt


def ordre_decr(f):
    """ énumère les sommets selon la date f(_) par ordre décroissant.
    f : tableau tq f[i] = f(i)"""
    n = len(f)
    f_1 = []
    dv = [True for _ in range(n)]#tableau des déja vus.
    min_max = max(f)
    for i in range(n-1):#le ième plus gd temps de fin de parcours
        indice = -1
        val = -1
        for t in range(0,len(f)):
            if dv[t]:
                if f[t] > val:
                    dv[indice] = True
                    indice = t
                    val = f[t]
                    dv[t] = False
        f_1.append(indice)
    for j in range(n):
        if dv[j]:
            f_1.append(j)
    return f_1

    
def od(f):
    """ f = [5,12,-1,2,3,7]
    od(f) = [1,5,0,4,3,2]
    
    il s'agit d'une autre version de ordre_decr, utilisant un tri insertion en O(S²)"""
    def comp(a,b):
        """true iff f[a] < f[b]"""
        return f[a] < f[b]
    n = len(f)
    odf = list(range(n))
    for k in range(n):
        i = k  
        while comp(odf[i],odf[i - 1]) and i > 0:
            odf[i] += odf[i - 1]
            odf[i - 1] = odf[i] - odf[i - 1]#interversion
            odf[i] -= odf[i - 1]
            i -= 1
    return odf

def cfc(G):#algorithme pour graphes orientés
    """Algorithme de Kosaraju-Sharir"""
    n = len(G)
    d,f = pptime(G)
    rf = ordre_decr(f)
    arbres = pp_arbres_parcours(transpose_grp(G),rf)
    return arbres





## tests




""" autre version de l'algorithme
def ordre_decr(f):
    # énumère les sommets selon la date f(_) par ordre décroissant.
    #f : tableau tq f[i] = f(i)
    f_1 = []
    f2 = f[:]#copie
    min_max = max(f2)
    n = len(f)
    for i in range(n):#le ième plus gd temps de fin de parcours
        indice = 0
        for t in range(1,len(f2)):
            if f2[t] > f2[indice]:
                indice = t
        f2.remove(f2[indice])
        f_1.append(indice)
    f3=f_1[:]
    for t in range(n):
        for x in range(t):
            if f_1[x] +1 <= f_1[t]:
                f_1[t] += 1
    return f_1, f3
"""   
     

## 2PAC
"""
def pointartic(G):
    #  détermine les points d'articulation
    PA = [False in range(len(G))]
    t = 0
    PI = [None in range(len(G))]
    def pac2(G, v):
        n = len(G)
        t += 1
        Couleur[v] = "gris"# = ["gris" for _ in range(n)]
        d[v] = t
        Low[v] = d[v]
        nbfils = 0
        for w in G[v]:
            if Couleur[w] == "blanc":
                PI[w] = v
                nbfils += 1
                pac2(G,w)
                if (PI[v] != None) and Low[w] >= d[v]:
                    PA[v] = True
                Low[v] = min(Low[v],Low[w])
                
            elif (w != PI[v]):
                Low[v] = min(Low[v],d[w])
            
        if PI[v] == None and nbfils > 0:
            PA[v] = True#0 ou 1 ???
    
    for tau in range(len(G)):
        if not PA[tau] :
            pac2(G,tau)


"""
##
class file:
    def __init__(self):
        self.inn = []
        self.out = []
    def empty(self):
        return self.inn == [] and self.out == []
    def pop(self):
        assert not self.empty()
        if self.out == []:
            while self.inn != []:
                e = self.inn.pop()
                self.out.append(e)
            return e
        else:
            return self.out.pop()
    def push(self,e):
        self.inn.append(e)
        
class tas:
    def __init__(self):
        """ crée une file de priorité en O(1) """
        self.T = [[None,None]]
        self.d = dict()#emplacements
        self.nb = 0
        
    def insert(self,key=0,value='Value'):
        """insère une nouvelle valeur en O(log(n))"""
        self.nb += 1
        i = self.nb#on commence à 1
        while i >= len(self.T):
            self.T.append([key,value])
        while (i//2 > 1) and (self.T[i//2][0] > key):
            self.T[i] = self.T[i//2]#prop du tas
            i //= 2
        if self.nb >= len(self.T):
            #self.T.append([key,value])
            pass
        else:
            self.T[i] = [key,value]
        self.d[value] = i
        
    def percolation(self,i):
        """ rétablit les propriétés du tas O(log(n))"""
        ancien_i = i
        g = 2 * i
        d = 2 * i + 1
        if g < self.nb and self.T[g][0] < self.T[i][0]:i = g
        if d < self.nb and self.T[d][0] < self.T[i][0]:i = d
        if i != ancien_i:#trouvé un fils ne respectant pas la propriété du tas
            ti = self.T[i]
            self.d[self.T[i][1]] = ancien_i
            self.d[self.T[ancien_i][1]] = i
            self.T[i] = self.T[ancien_i]
            self.T[ancien_i] = ti
            self.percolation(i)
            
    def extraitMin(self):
        """extrait le minimum O(log(n))"""
        mini = self.T[1][1]#value of the min -> key is not important
        self.T[1] = self.T[self.nb]
        self.d[self.T[1][1]] = 1
        self.nb -= 1
        self.percolation(1)
        return mini
    
    def pop(self):#alias
        return self.extraitMin()    
    def modify(self,cle,v):#alias
        return self.decreasekey(v,cle)
    def add(self,e):#alias
        return self.insert(e[0],e[1])
    def empty(self):
        return self.nb == 0
    def contains(self,v):
        """ Teste si la file contient un élément : O(1) """
        return v in self.d 
    def initialise(self,L):
        """Initialise le tas en O(n)"""
        self.T = L
        self.nb = len(L)
        i = np.floor(len(L)/2)
        while i >= 1:
            percolation(i)
            i -= 1
    
    def decreasekey(self,value,new_key):
        self.T[self.d[value]][0] = new_key
        self.percolation(self.d[value])
        
    def __repr__(self):
        return "tas:"+str(self.T)
tau = tas()
for k in range(10):
    tau.insert(k*k,str(k)+"k!")
